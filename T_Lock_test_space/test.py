from typing import Pattern
import zipfile
import base64
from tkinter.filedialog import askopenfilenames
import time
import os
from tkinter import Tk
import random
import re


def base64_encode(file) -> bytes:
    with open(file, 'rb')as file:
        file = file.read()
        file = base64.b64encode(file)
        return file


def get_info(file) -> dict:
    ctime = os.path.getctime(file)
    atime = os.path.getatime(file)
    mtime = os.path.getmtime(file)
    size = os.path.getsize(file)
    return {'ctime': ctime, 'atime': atime, 'mtime': mtime, 'size': size}


def encode(b64: bytes, info: dict):
    key = str(time.time()-info['ctime']).split('.')[0]
    print(key)
    while(len(key) % 4 != 0):
        key = ''.join(['0', key])
    key = ''.join([key, 'j200tkj9'])
    key = ''.join(['0c+2ns9e', key])
    # print(key.encode())
    len_of_b64 = len(b64)
    ran = random.randrange(0, len(b64))
    # print(ran)
    part_1 = b64[0: ran]
    part_2 = b64[ran:len_of_b64]
    # print(b64 == b''.join([part_1, part_2]))
    final = b''.join([part_1, key.encode(), part_2])
    final = base64.b16encode(final)[::-1]
    with open('test.lock', 'wb')as file:
        file.write(final)
    with zipfile.ZipFile('test.zip', 'w')as ziped:
        ziped.write('test.lock')

    with open(r'C:\Users\16418\Pictures\Video Projects\fzzl.png', 'rb')as icon:
        with open('test.zip','rb')as zip:
            with open('fzzl.png','wb')as out:
                out.write(b''.join([icon.read(),zip.read()]))
def main():
    Tk().withdraw()
    files = askopenfilenames()
    # print(files)
    for x in files:
        x_b64 = base64_encode(x)
        encode(x_b64, get_info(x))
        # print(x)
        # print(get_info(x))


main()
