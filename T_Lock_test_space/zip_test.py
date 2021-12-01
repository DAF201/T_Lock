import zipfile
with zipfile.ZipFile('test.zip', 'w')as zip_test:
    zip_test.write(r'C:\Users\work_space\python\T_Lock\test.py')
with open(r'C:\Users\16418\Pictures\Video Projects\fzzl.png', 'rb')as photo:
    with open('test.zip', 'rb')as zip:
        with open('final.png', 'wb')as final:
            photo = photo.read()
            zip = zip.read()
            res = b''.join([photo, zip])
            final.write(res)
