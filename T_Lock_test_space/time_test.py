import time
import os
a = os.path.getatime(r'Java\helloWorld.java')
print(a)
print(time.ctime(a))
with open(r'Java\helloWorld.java', 'a')as file:
    file.write('\nhello')
print(time.ctime(os.path.getatime(r'Java\helloWorld.java')))
os.utime(r'Java\helloWorld.java',(a,a))
print(time.ctime(os.path.getatime(r'Java\helloWorld.java')))
print(os.path.getatime(r'Java\helloWorld.java'))

# access access time will not change access time
# write or read will change access time
# utime can change access time