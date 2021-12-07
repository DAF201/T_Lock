import base64
from tkinter.filedialog import askopenfilenames
import time
import os
from tkinter import Tk
import hashlib
import json
import zipfile
import random
from os.path import basename


class FileError(Exception):
    def __init__(self, message='an unexpected exception about the file happened'):
        super().__init__(message)


class TimeOutError(Exception):
    def __init__(self, message='this file as expired: '):
        super().__init__(message)


class LockingError(Exception):
    def __init__(self, message='an error happened during creating the lock'):
        super().__init__(message)


class file:
    def __init__(self, path: os.path) -> None:
        self._path = path
        self._size = os.path.getsize(path)
        self._create_time = os.path.getctime(path)
        self._access_time = os.path.getatime(path)
        self._modify_time = os.path.getmtime(path)
        self._name = os.path.splitext(path)[0].split('/')[-1]
        self._extension = os.path.splitext(path)[1]


class Lock(file):
    def __init__(self, path: os.path) -> None:
        super().__init__(path)

    @property
    def base_data(self):
        with open(self._path, 'rb')as current_file:
            base_data = base64.b16encode(current_file.read())
        return base_data

    @property
    def key(self):
        pass


class normalFile(file):
    def __init__(self) -> None:
        super().__init__()


def main():
    Tk().withdraw()
    files = askopenfilenames()
    for x in files:
        Lock(x)


if __name__ == '__main__':
    main()
