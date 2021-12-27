import sys
import ctypes
import os
import time
import zipfile
from tkinter.filedialog import askopenfilenames
import json
from tkinter import Tk
import glob
import threading

if ctypes.windll.shell32.IsUserAnAdmin():
    pass
else:
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, __file__, None, 1)
    time.sleep(3)
    os._exit(0)

flag = True


class locked:
    def __init__(self, path) -> None:
        global flag
        self.__flag = True
        self.__path = path
        self.__name = os.path.basename(self.__path).split('.')[0]
        self.__check_name()
        if self.__flag:
            self.__create_key()
            self.__unlock()
            self.__pack_up()
            flag = False
        else:
            flag = False
            os._exit(0)

    def __check_name(self):
        try:
            with zipfile.ZipFile(self.__path, 'r')as zip:
                zip.extract(self.__name+'.json')
            with open(self.__name, 'r')as json_data:
                self.__json_data = json.load(json_data)
        except:
            with zipfile.ZipFile(self.__path, 'r')as zip:
                zip.extractall()
        with open(self.__last_file('.json'), 'r')as json_data:
            self.__json_data = json.load(json_data)
        if (time.time() > self.__json_data['time']['expire']) or (self.__json_data['time']['now'] > time.time()):
            print('file is no longer available. @ %s' %
                  time.ctime(self.__json_data['time']['expire']))
            self.__flag = False
            time.sleep(5)
            os.remove(self.__last_file('.lock'))
        os.remove(self.__last_file('.json'))

    def __create_key(self):
        self.__key = int((self.__json_data['time']['atime'] +
                         self.__json_data['time']['ctime']+self.__json_data['time']['mtime']) % 128)

    def __unlock(self):
        with open(self.__last_file('.lock'), 'rb')as lock:
            self.__data = lock.read()
        self.__data = list(self.__data)
        for x in range(len(self.__data)):
            if self.__data[x] == 255:
                self.__data[x] = 0
            elif self.__data[x] <= self.__key:
                self.__data[x] = 255+self.__data[x]-self.__key
            else:
                self.__data[x] -= self.__key

    def __pack_up(self):
        with open(self.__json_data['name']+self.__json_data['ext'], 'wb')as final:
            final.write(bytes(self.__data))
        os.remove(self.__json_data['name']+'.lock')

    def __last_file(self, ext):
        list_of_files = glob.glob('*%s' % ext)
        latest_file = max(list_of_files, key=os.path.getctime)
        return latest_file


class normal:
    def __init__(self, path) -> None:

        self.__get_config()
        self.__cover = self.__config['cover']

        self.__path = path
        self.__name = os.path.basename(self.__path).split('.')[0]
        self.__ext = os.path.splitext(self.__path)[1]

        self.__file_info()
        self.__file_data()
        self.__file = {
            'name': self.__name,
            'ext': self.__ext,
            'time': self.__time
        }

        self.__add_key()
        self.__save_data()
        self.__pack_up()

    def __file_data(self):
        with open(self.__path, 'rb')as file:
            self.__data = file.read()

    def __get_config(self):
        try:
            with open('config.json', 'r')as json_data:
                self.__config = json.load(json_data)
        except:
            config = {
                'hours': 48,
                'cover': 'cover.gif',
                'output': ''
            }
            with open('config.json', 'w')as json_data:
                json.dump(config, json_data)
            self.__config = config

    def __file_info(self):
        atime = os.path.getatime(self.__path)
        ctime = os.path.getctime(self.__path)
        mtime = os.path.getmtime(self.__path)
        now = time.time()
        self.__time = {
            'atime': atime,
            'ctime': ctime,
            'mtime': mtime,
            'now': now,
            'expire': now+3600*self.__config['hours']
        }
        self.__key = int((atime+ctime+mtime) % 128)

    def __add_key(self):
        self.__data = list(self.__data)
        length = len(self.__data)
        # print(list_data)
        for x in range(len(self.__data)):
            temp = self.__data[x]+self.__key
            if self.__data[x] == 0:
                self.__data[x] = 255
            elif temp >= 255:
                self.__data[x] = temp-255
            else:
                self.__data[x] = temp

    def __save_data(self):
        with open(self.__name+'.json', 'w')as file_json:
            json.dump(self.__file, file_json)

    def __pack_up(self):
        with open(self.__name+'.lock', 'wb')as lock:
            lock.write(bytes(self.__data))
        with zipfile.ZipFile(self.__name+'.zip', 'w')as zip:
            zip.write(self.__name+'.lock',
                      os.path.basename(self.__name+'.lock'))
            zip.write(self.__name+'.json',
                      os.path.basename(self.__name+'.json'))
        with open(self.__name+'.zip', 'rb')as zip:
            with open(self.__cover, 'rb')as cover:
                with open(self.__name+'.lock.'+self.__cover.split('.')[1], 'wb')as final:
                    final.write(cover.read()+zip.read())
        os.remove(self.__name+'.zip')
        os.remove(self.__name+'.lock')
        os.remove(self.__name+'.json')
        global flag
        flag = False


def timing():
    now = time.time()
    print('started!')
    while(flag):
        print('time cost: %s' % (time.time()-now), end='\r')
        time.sleep(0.1)
    print('finished!')


def main():
    def check(file) -> bool:
        ext = os.path.splitext(file)[1]
        extension = iter(
            ['.bmp', '.jpg', '.png', '.tif', '.gif', '.pcx', '.tga', '.exif', '.fpx', '.svg', '.psd', '.cdr', '.pcd', '.dxf', '.ufo', '.eps', '.ai', '.raw', '.WMF', '.webp', '.avif', '.apng'])
        flag = 0
        if ext in extension:
            if zipfile.is_zipfile(file):
                flag = 1
        return flag
    global flag
    Tk().withdraw()
    files = askopenfilenames()
    for file in files:
        flag = True
        threading.Thread(target=timing).start()
        print()
        if check(file):
            locked(file)
        else:
            normal(file)
        time.sleep(0.1)
    time.sleep(3)


main()
