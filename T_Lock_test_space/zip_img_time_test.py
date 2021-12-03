import zipfile
import os
print(os.path.getctime('t.py'))
print(os.path.getatime('t.py'))
print(os.path.getmtime('t.py'))

with zipfile.ZipFile('t.zip', 'w')as zip:
    zip.write('t.py')
os.remove('t.py')
with open('default_image.jpg', 'rb')as img:
    with open('t.zip', 'rb')as zip:
        zipbytes = zip.read()
        imgbytes = img.read()


os.remove('t.zip')


with open('t.jpg', 'wb')as zip:
    zip.write(b''.join([zipbytes, imgbytes]))

file = 't.jpg'
base = file.split('.')[0]
os.rename(file, base+'.zip')

with zipfile.ZipFile('t.zip', 'r')as zip:
    zip.extractall()


print(os.path.getctime('t.py'))
print(os.path.getatime('t.py'))
print(os.path.getmtime('t.py'))

# zip and unzip
# 1638554353.9925392
# 1638554353.9925392
# 1638554353.9925392

# 1638554353.9925392
# 1638554737.7964416
# 1638554737.7964416
