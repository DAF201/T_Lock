import os
import zipfile
from os.path import basename
PATH = r'C:\Users\work_space\python\T_Lock_test_space\test.txt'
# with zipfile.ZipFile('zip_test.zip', 'w')as zip:
#     zip.write(PATH,basename(PATH))
# os.remove(PATH)
# import time
# time.sleep(3)
# with zipfile.ZipFile('zip_test.zip', 'r')as zip:
#     zip.extractall(r'C:\Users\work_space\python\T_Lock_test_space')
print('ctime:'+str(os.path.getctime(PATH)))
print('atime:'+str(os.path.getatime(PATH)))
print('mtime:'+str(os.path.getmtime(PATH)))
# original
# ctime:1638552613.938337
# atime:1638552702.4999843
# mtime:1638552702.1688392

# zip and unzip
# ctime:1638552613.938337
# atime:1638552749.4763527
# mtime:1638552749.4763527


# remains are manually unzip tested

# copy the zip and unzip
# ctime:1638552809.9640555
# atime:1638552810.8119593
# mtime:1638552702.0

# cut the zip and unzip

# ctime:1638552809.9640555
# atime:1638552880.299896
# mtime:1638552702.0

# upload and download and move to here
# ctime:1638553022.1430767
# atime:1638553022.222452
# mtime:1638552702.0
