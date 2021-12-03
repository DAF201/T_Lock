import zipfile
import os
print(os.path.getctime('t.py'))
print(os.path.getatime('t.py'))
print(os.path.getmtime('t.py'))
with zipfile.ZipFile('t.zip', 'w')as zip:
    zip.write('t.py')
os.remove('t.py')
with zipfile.ZipFile('t.zip', 'r')as zip:
    zip.extractall()
print(os.path.getctime('t.py'))
print(os.path.getatime('t.py'))
print(os.path.getmtime('t.py'))

# zip and un zip

# 1638553612.7103932 ctime
# 1638553612.7103932 atime
# 1638553612.7103932 mtime

# 1638553612.7103932
# 1638553790.0718744
# 1638553790.0718744

# zip, move, move back and unzip

# 1638553612.7103932
# 1638553790.0718744
# 1638553790.0718744

# 1638553950.1049001
# 1638553950.1049001
# 1638553950.1049001

# zip, cut, past, cut, past back and unzip
# 1638553950.1049001
# 1638553950.1049001
# 1638553950.1049001

# 1638554081.4225059
# 1638554081.4225059
# 1638554081.4225059
