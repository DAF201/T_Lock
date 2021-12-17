import os
from os.path import getatime, getctime, getmtime, splitext
from time import time
from zipfile import ZipFile as zip
from zipfile import is_zipfile as is_zip
from hashlib import sha256
from json import load, dump
from tkinter import Tk
from tkinter.filedialog import askopenfilenames
from glob import glob
from threading import Thread

run = True


def last_file(directory, extension='jpg') -> os.path:
    '''get the last file in extension,default extension: jpg, last_file(directory,extension)->path'''
    list_of_files = glob(''.join([directory, '\\*.%s' % extension]))
    try:
        last_file = max(list_of_files, key=getctime)
        return last_file
    except:
        return None


class file:
    '''general file, file(path)'''

    def __init__(self, _path) -> None:
        '''create general data'''
        self._path = _path

        self._name = splitext(self._path)[0].split('/')[-1]
        self._ext = splitext(self._path)[1]

        self._ctime = getctime(self._path)
        self._atime = getatime(self._path)
        self._mtime = getmtime(self._path)
        self._current_time = time()

        with open(self._path, 'rb')as file:
            self._data = file.read()
            self._sha256 = sha256(self._data).hexdigest()
        self._half = int(len(self._data)/2)

    def _hash(self, data):
        if type(data) == str:
            return sha256(data.encode()).hexdigest()
        if type(data) == bytes:
            return sha256(data).hexdigest()

    def _timeing(self):
        import time
        start = time.time()
        while run:
            print('time cost: %s' % (time.time()-start), end='\r')
            time.sleep(0.1)


class locked(file):
    '''locked file, locked(path)'''

    def __init__(self, path) -> None:
        super().__init__(path)
        self.f = Thread(target=self.__main)
        self.t = Thread(target=self._timeing)

        self.f.start()
        self.t.start()
        self.f.join()
        self.t.join()

    def __get_json_info(self):
        with zip(self._path)as zipped:
            zip.extractall(zipped)
        self.__work_space = os.getcwd()
        with open(last_file(self.__work_space, extension='json'), 'r')as json_data:
            self.__json = load(json_data)
        with open(last_file(self.__work_space, extension='lock'), 'rb')as lock:
            self.__lock = lock.read()
        os.remove(last_file(self.__work_space, extension='json'))
        os.remove(last_file(self.__work_space, extension='lock'))

    def __get_key(self):
        self.__key = int(self.__json['atime'] +
                         self.__json['ctime']+self.__json['mtime']) % 8

    def __generate(self):
        self.__lock = list(self.__lock)
        for x in range(len(self.__lock)):
            if 256-self.__lock[x] > self.__key:
                self.__lock[x] -= self.__key
        self.__lock = bytes(self.__lock)

    def __create(self):
        with open(''.join([self.__work_space, '\\', self.__json['name'], self.__json['ext']]), 'wb')as final:
            final.write(self.__lock)

    def __main(self):
        print('decoding: %s' % (self._name+self._ext))
        self.__get_json_info()
        self.__get_key()
        self.__generate()
        if self.check:
            self.__create()
        global run
        run = False

    @property
    def check(self):
        self._half = int(len(self.__lock)/2)
        cal_key_hash = b''.join([self.__lock[self._half-32:self._half],
                                 self.__lock[self._half: self._half+32]])
        key_hash = self._hash(str(self.__json)).encode()

        self.__lock = self.__lock.replace(cal_key_hash, b'')
        return (cal_key_hash == key_hash) | (sha256(self.__lock).hexdigest() == self.__json['hash']) | (self.__json['expire_time'] > time())


class normal(file):
    '''not locked file, normal(path)'''

    def __init__(self, path) -> None:
        super().__init__(path)

        default_image = ''.join(
            [__file__.replace('T_Lock_for_ASCII.py', ''), 'default_image.jpg'])
        try:
            with open('customize.json', 'r')as customize:
                self.customize = load(customize)
        except:

            self.customize = {
                'cover': default_image,
                'expire_hours': 48
            }
            with open('customize.json', 'w')as customize:
                dump(self.customize, customize)

        self.__hash = self._hash(self._data)

        self.__key = int(self._atime+self._ctime+self._mtime) % 8
        self.__key_dict = {
            'name': self._name,
            'ext': self._ext,
            'atime': self._atime,
            'ctime': self._ctime,
            'mtime': self._mtime,
            'current_time': self._current_time,
            'expire_time': self._current_time+3600*self.customize['expire_hours'],
            'hash': self.__hash
        }

        self.__key_hash = self._hash(str(self.__key_dict)).encode()

        print('encoding: %s' % (self._name+self._ext))
        self.f = Thread(target=self.__main)
        self.t = Thread(target=self._timeing)

        self.f.start()
        self.t.start()
        self.f.join()
        self.t.join()

    def __main(self):
        self.__insert_key_hash()
        self.__add_key()
        self.__create_lock()
        self.__zip()
        self.__merge()
        global run
        run = False

    def __add_key(self):

        self._data = list(self._data)
        for x in range(len(self._data)):
            if self._data[x]+self.__key < 256:
                self._data[x] += self.__key
        self._data = bytes(self._data)

    def __insert_key_hash(self):
        p1, p2 = self._data[0:self._half], self._data[self._half:len(
            self._data)]
        self._data = b''.join([p1, self.__key_hash, p2])
        with open('t.py', 'wb')as test:
            test.write(self._data)

    def __create_lock(self):
        with open(''.join([self._name, '.lock']), 'wb')as lock:
            lock.write(self._data)
        with open(''.join([self._name, '.json']), 'w')as info:
            dump(self.__key_dict, info)

    def __zip(self):
        with zip(''.join([self._name, '.zip']), 'w')as zipped:
            zipped.write(''.join([self._name, '.lock']))
            zipped.write(''.join([self._name, '.json']))
        os.remove(''.join([self._name, '.lock']))
        os.remove(''.join([self._name, '.json']))

    def __merge(self):
        with open(''.join([self._name, '.zip']), 'rb')as zipped:
            with open(self.customize['cover'], 'rb')as cover:
                with open(''.join([self._name, '.jpg']), 'wb')as final:
                    final.write(b''.join([cover.read(), zipped.read()]))
        os.remove(''.join([self._name, '.zip']))


def main():
    '''main function'''
    def check(file) -> bool:
        '''check if a file was locked or not, check(path) -> 0 or 1'''
        ext = splitext(file)[1]
        extension = iter(
            ['.bmp', '.jpg', '.png', '.tif', '.gif', '.pcx', '.tga', '.exif', '.fpx', '.svg', '.psd', '.cdr', '.pcd', '.dxf', '.ufo', '.eps', '.ai', '.raw', '.WMF', '.webp', '.avif', '.apng'])
        is_img = 0
        flag = 0
        if ext in extension:
            is_img = 1
        if is_img:
            if is_zip(file):
                flag = 1
        return flag
    Tk().withdraw()
    files = askopenfilenames()
    for file in files:
        if check(file):
            locked(file)
        else:
            normal(file)


if __name__ == '__main__':
    main()
