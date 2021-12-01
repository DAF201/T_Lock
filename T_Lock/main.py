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


class TimeError(Exception):
    def __init__(self, message='this file as expired: '):
        super().__init__(message)


class LockingError(Exception):
    def __init__(self, message='an error happened during the locking'):
        super().__init__(message)


class file:
    def __init__(self, path: str):
        try:
            self.path = path
            self.name_and_extension = self.path.split('/')[-1].split('.')
            self.info = {
                'size':
                str(os.path.getsize(self.path)),
                'atime':
                str(os.path.getatime(self.path)).split('.')[0],
                'ctime':
                str(os.path.getctime(self.path)).split('.')[0],
                'mtime':
                str(os.path.getmtime(self.path)).split('.')[0],
                'file_name':
                self.name_and_extension[0],
                'file_extension':
                self.name_and_extension[1]
            }
            with open(path, 'rb')as file:
                self.data = base64.b16encode(
                    str(base64.b64encode(file.read())).encode())
        except:
            raise FileError


class locked(file):
    def __init__(self, path: str):
        super().__init__(path)
        if self.check() != True:
            raise FileError
        else:
            self.unlock()

    def unlock(self):
        pass

    def check(self):
        return


class normal(file):
    def __init__(self, path: str):
        super().__init__(path)

        self.output_info = {
            'source_dir':
            ''.join([__file__.split('\main.py')[0], '\Source']),
            'output_dir':
            ''.join([__file__.split('\main.py')[0], '\Output'])
        }
        self.lock

    @property
    def lock(self):
        try:
            self.info['expire_key'] = str(

                int(str(time.time()).split('.')[0])+(3600*24*2))

            json_path = self.output_info['output_dir'] + \
                '/'+self.info['file_name']+'.json'
            lock_path = self.output_info['output_dir'] + \
                '/'+self.info['file_name']+'.lock'
            zip_path = self.output_info['output_dir'] + \
                '/'+self.info['file_name']+'.zip'
            image_path = self.output_info['source_dir']+'/default_image.jpg'
            output_path = self.output_info['output_dir'] + \
                '/'+self.info['file_name']+'.jpg'

            with open(json_path, 'w')as json_file:
                json.dump(self.info, json_file)

            self.local_key = base64.b16encode(hashlib.sha256(
                str(self.info).encode()).hexdigest().encode())

            position = random.randrange(0, len(self.data))
            part1, part2 = self.data[0:position], self.data[position:len(
                self.data)]

            self.data = b''.join([part1, self.local_key, part2])

            position = random.randrange(0, len(self.data))

            ctime_key = base64.b16encode(str(os.path.getctime(
                json_path)).encode())

            part1, part2 = self.data[0:position], self.data[position:len(
                self.data)]

            self.data = b''.join([part1, ctime_key, part2])

            data = b' '.join(self.data[i:i+2]
                             for i in range(0, len(self.data), 2))

            with open(lock_path, 'wb')as lock:
                lock.write(data)

            os.utime(
                lock_path, (int(self.info['atime']), int(self.info['mtime'])))

            with zipfile.ZipFile(
                    zip_path, 'w')as zipping:
                zipping.write(lock_path, basename(lock_path))
                zipping.write(json_path, basename(json_path))

            with open(zip_path, 'rb')as zipping:
                with open(image_path, 'rb')as image:
                    with open(output_path, 'wb')as output:
                        output.write(b''.join([image.read(), zipping.read()]))

            os.remove(lock_path)
            os.remove(json_path)
            os.remove(zip_path)
        except:
            raise LockingError


def main():
    Tk().withdraw()
    files = askopenfilenames()
    for x in files:
        normal(x)


if __name__ == '__main__':
    main()
