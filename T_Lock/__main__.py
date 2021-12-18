import os
from os.path import basename
import time
import zipfile
from tkinter import Tk
import hashlib
import base64
import random
import json
from tkinter.filedialog import askopenfilenames
import glob

'''output path'''
OUTPUT = ''.join([__file__.split('__main__.py')[0], 'output\\'])

'''customize data path'''
with open(''.join([__file__.split('__main__.py')[0], '\\customize\\customize.json'])) as customize:
    CUSTOMIZE = json.load(customize)

EXPIRE_TIME = int(CUSTOMIZE['hours'])
if EXPIRE_TIME <= 0:
    EXPIRE_TIME = 1


class CoverError(Exception):
    '''can not find the customizing cover'''

    def __init__(self, *arg) -> None:
        super().__init__(''.join(
            ['\n\tan unexpected error occurred while trying find the customized cover: ',
                str(arg)]
        ))


def cover(cover):
    '''get cover path, return default cover when running into an error'''
    try:
        list_of_files = glob.glob(''.join([cover, '*%s' % CUSTOMIZE['cover']]))
        cover = max(list_of_files, key=os.path.getctime)
        return cover
    except Exception as error:
        print('error: '+str(CoverError(error)), 'using default cover instead')
        return ''.join([__file__.split('__main__.py')[0], 'source\\default_image.jpg'])


'''cover path'''
COVER = cover(''.join([__file__.split('__main__.py')[0], 'source\\']))


'''temporary path'''
TEMP = ''.join([__file__.split('__main__.py')[0], 'temp\\'])


def TEMP_JSON(name):
    '''temporary json path'''
    return ''.join([TEMP, name, '.json'])


def TEMP_LOCK(name):
    '''temporary lock path'''
    return ''.join([TEMP, name, '.lock'])


def TEMP_ZIP(name):
    '''temporary zip path'''
    return ''.join([TEMP, name, '.zip'])


class InitError(Exception):
    '''fail to initialize'''

    def __init__(self, *arg) -> None:
        super().__init__(''.join(
            ['\n\tan unexpected error occurred while initializing: ',
                str(arg)]
        ))


class BaseError(Exception):
    '''fail to make base data'''

    def __init__(self, *arg) -> None:
        super().__init__(''.join(
            ['\n\tan unexpected error occurred while encoding/decoding of the data: ',
                str(arg)]
        ))


class HashError(Exception):
    '''fail to make hash data'''

    def __init__(self, *arg) -> None:
        super().__init__(''.join(
            ['\n\tan unexpected error occurred while creating of the hash: ',
                str(arg)]
        ))


class VerifyError(Exception):
    '''fail to verify the file'''

    def __init__(self, *args: object, message) -> None:
        super().__init__(
            ''.join(['an unexpected error occurred while vertifying: ', str(args), ' ', message]))


class file:
    '''general file'''

    def __init__(self, path) -> None:
        '''file initializing'''
        try:
            '''basic info about the file'''

            self._path = str(path)
            self._name = str(self._path.split('/')[-1].split('.')[0])
            self._ext = ''.join(['.', self._path.split('/')[-1].split('.')[1]])
            self._time_info = {
                'ctime': int(str(os.path.getctime(self._path)).split('.')[0]),
                'mtime': int(str(os.path.getmtime(self._path)).split('.')[0]),
                'atime': int(str(os.path.getatime(self._path)).split('.')[0]),
                'now': int(str(time.time()).split('.')[0])
            }
        except Exception as exc:
            raise InitError(exc)

        '''base16 info of the file'''
        try:
            with open(self._path, 'rb')as file:
                self._base64_data = base64.b64encode(file.read())
        except Exception as exc:
            raise BaseError(exc)


class normal(file):
    '''process normal file'''

    def __init__(self, path) -> None:
        super().__init__(path)

        try:
            '''create hash of original file'''
            self.__hash = hashlib.sha256(
                self._base64_data).hexdigest()
        except Exception as error:
            raise HashError(error)

        '''create json copy'''
        self.__json_data = {
            'name': self._name,
            'extension': self._ext,
            'time_info': self._time_info,
            'hash_info': self.__hash,
            'expire_time': self._time_info['now']+3600*EXPIRE_TIME,
        }
        self.__json_hash = hashlib.sha256(
            str(self.__json_data).encode()).hexdigest()

        '''dump json'''
        with open(TEMP_JSON(self._name), 'w')as data:
            json.dump(self.__json_data, data)

        '''create key'''
        self.__key = int((
            self.__json_data['time_info']['atime']
            + self.__json_data['time_info']['ctime']
            + self.__json_data['time_info']['mtime']
            + self.__json_data['time_info']['now']
        ) % 8)

        '''generating basedata list'''
        point1, point2, point3, point4, point5, point6 = 0, 0, 0, 0, 0, 0
        while(point1 == point2 == point3 == point4 == point5 == point6):
            point1 = random.randrange(len(self._base64_data))
            point2 = random.randrange(len(self._base64_data))
            point3 = random.randrange(len(self._base64_data))
            point4 = random.randrange(len(self._base64_data))
            point5 = random.randrange(len(self._base64_data))
            point6 = random.randrange(len(self._base64_data))
        points = [point1, point2, point3, point4, point5, point6]
        points.sort()

        '''creating slices'''
        p1 = self._base64_data[0:points[0]]
        p2 = self._base64_data[points[0]:points[1]]
        p3 = self._base64_data[points[1]:points[2]]
        p4 = self._base64_data[points[2]:points[3]]
        p5 = self._base64_data[points[3]:points[4]]
        p6 = self._base64_data[points[4]:points[5]]
        p7 = self._base64_data[points[5]:len(self._base64_data)]

        '''insert data'''
        self._base64_data = (p1+str(
            self._time_info['ctime']).encode()+p2+str(
            self._time_info['atime']).encode()+p3+str(
            self._time_info['mtime']).encode()+p4+str(
            self._time_info['now']).encode()
            + p5+self.__json_hash.encode()
            + p6+str(self.__json_data['expire_time']).encode()
            + p7)

        '''convert to base16'''
        self._base64_data = base64.b16encode(self._base64_data)

        '''add key to it'''
        self._base64_data = list(self._base64_data)

        for x in range(len(self._base64_data)):
            self._base64_data[x] += self.__key

        self._base64_data = bytes(self._base64_data)

        '''prettify'''
        self._base64_data = b'\n'.join(
            self._base64_data[i: i+41] for i in range(0, len(self._base64_data), 41))
        self._base64_data = b' '.join(
            self._base64_data[i: i+2] for i in range(0, len(self._base64_data), 2))
        self._base64_data = b''.join([b' ', self._base64_data])

        '''write lock'''
        with open(TEMP+self._name+'.lock', 'wb')as lock:
            lock.write(self._base64_data)

        '''create zip'''
        with zipfile.ZipFile(TEMP+self._name+'.zip', 'w')as zip:
            zip.write(TEMP+self._name+'.lock',
                      basename(TEMP+self._name+'.lock'))
            zip.write(TEMP+self._name+'.json',
                      basename(TEMP+self._name+'.json'))

        '''remove temporary files'''
        os.remove(TEMP+self._name+'.lock')
        os.remove(TEMP+self._name+'.json')

        '''bind zip to cover'''
        with open(TEMP+self._name+'.zip', 'rb')as zip:
            with open(COVER, 'rb')as cover:
                with open(OUTPUT+self._name+CUSTOMIZE['cover'], 'wb')as final:
                    final.write(b''.join([cover.read(), zip.read()]))

        '''remove temporary zip'''
        os.remove(TEMP+self._name+'.zip')

        '''print expire time'''
        print(''.join(['file will expire at: ', time.ctime(
            self.__json_data['expire_time']), ' keep eye on time']))


class locked(file):
    '''process locked file'''

    def __init__(self, path) -> None:
        super().__init__(path)

        '''unzip'''
        with zipfile.ZipFile(self._path, 'r')as zip:
            zip.extractall(TEMP)
        with open(TEMP+self._name+'.json', 'r')as json_data:
            self.__json_data = json.load(json_data)
        with open(TEMP+self._name+'.lock', 'rb')as lock_data:
            self.__lock_data = lock_data.read()

        '''remove temporary files'''
        os.remove(TEMP+self._name+'.json')
        os.remove(TEMP+self._name+'.lock')

        '''generate key'''
        self.__key = int((
            self.__json_data['time_info']['atime']
            + self.__json_data['time_info']['ctime']
            + self.__json_data['time_info']['mtime']
            + self.__json_data['time_info']['now']
        ) % 8)

        '''normalize'''
        self.__lock_data = self.__lock_data.replace(
            b' ', b'').replace(b'\n', b'')

        self.__lock_data = list(self.__lock_data)

        '''remove key'''
        for x in range(len(self.__lock_data)):
            self.__lock_data[x] -= self.__key
        self.__lock_data = bytes(self.__lock_data)

        '''decode base16'''
        self.__lock_data = base64.b16decode(self.__lock_data)

        '''check/remove data'''
        flag = True
        if str(self.__json_data['time_info']['atime']).encode() not in self.__lock_data:
            flag = False
            raise VerifyError(VerifyError, 'atime',
                              message='fail to verify the atime')
        else:
            self.__lock_data = self.__lock_data.replace(
                str(self.__json_data['time_info']['atime']).encode(), b'')

        if str(self.__json_data['time_info']['ctime']).encode() not in self.__lock_data:
            flag = False
            raise VerifyError(VerifyError, 'ctime',
                              message='fail to verify the ctime')
        else:
            self.__lock_data = self.__lock_data.replace(
                str(self.__json_data['time_info']['ctime']).encode(), b'')

        if str(self.__json_data['time_info']['mtime']).encode() not in self.__lock_data:
            flag = False
            raise VerifyError(VerifyError, 'mtime',
                              message='fail to verify the mtime')
        else:
            self.__lock_data = self.__lock_data.replace(
                str(self.__json_data['time_info']['mtime']).encode(), b'')

        if str(self.__json_data['time_info']['now']).encode() not in self.__lock_data:
            flag = False
            raise VerifyError(VerifyError, 'ptime',
                              message='fail to verify the process time')
        else:
            self.__lock_data = self.__lock_data.replace(
                str(self.__json_data['time_info']['now']).encode(), b'')

        if str(self.__json_data['expire_time']).encode() not in self.__lock_data:
            flag = False
            raise VerifyError(VerifyError, 'expire time',
                              message='fail to verify the expire time')
        else:
            self.__lock_data = self.__lock_data.replace(
                str(self.__json_data['expire_time']).encode(), b'')

        '''verify the key'''
        if hashlib.sha256(
                str(self.__json_data).encode()).hexdigest().encode() not in self.__lock_data:
            flag = False
            raise VerifyError(VerifyError, 'key',
                              message='fail to verify key')
        else:
            self.__lock_data = self.__lock_data.replace(
                hashlib.sha256(
                    str(self.__json_data).encode()).hexdigest().encode(), b'')

        '''verify the data'''
        if hashlib.sha256(
                self.__lock_data).hexdigest() != self.__json_data['hash_info']:
            flag = False
            raise VerifyError(VerifyError, 'lock',
                              message='fail to verify lock')

        '''check time'''
        if time.time() > self.__json_data['expire_time']:
            flag = False
            raise VerifyError(
                VerifyError, 'expired', message='file has expired! @%s' % self.__json_data['expire_time'])

        '''decode base64'''
        if flag:
            try:
                self.__lock_data = base64.b64decode(self.__lock_data)
                with open(OUTPUT+self.__json_data['name']+self.__json_data['extension'], 'wb')as final:
                    final.write(self.__lock_data)
            except Exception as error:
                raise error


def determine(file):
    if str(file).split('.')[-1] == 'jpg':
        if zipfile.is_zipfile(file):
            return True
        else:
            return False
    else:
        return False


def main():
    Tk().withdraw()
    files = askopenfilenames()
    for x in files:
        if determine(x):
            x = locked(x)
        else:
            x = normal(x)


if __name__ == '__main__':
    main()
