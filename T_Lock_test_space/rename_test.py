# #你好
# with open(r'C:\Users\work_space\python\T_Lock\test.py', 'rb')as file:
#     print(file.read())
import os
file = 'final.png'
base = file.split('.')[0]
os.rename(file,base+'.zip')
