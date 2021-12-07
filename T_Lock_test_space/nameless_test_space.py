# with open('test.lock','rb')as file:
#     data=file.read()[::-1]
# import base64
# data=base64.b16decode(data)
# a=data.index(b'j200tkj9')
# b=data.index(b'0c+2ns9e')
# c=data[b+8:a]
# c=int(c)
# print(c)
# import os
# a=os.path.getatime(r'C:\Users\work_space\python\T_Lock\Output\fzzl.lock')
# b=os.path.getmtime(r'C:\Users\work_space\python\T_Lock\Output\fzzl.lock')
# print(a,b)
# with open(r'C:\Users\16418\Downloads\mingw-get-setup.exe', 'rb')as file:
#     with open(r'C:\Users\16418\Desktop\important.zip', 'rb')as zipping:
#         with open('test.exe', 'wb')as final:
#             final.write(b''.join([file.read(), zipping.read()]))
import os
# print(
#     '''
#     json time: %s
#     lock time: %s
#     zip time: %s
#     jpg time: %s
#     ''' % ([os.path.getatime(r'C:\Users\work_space\python\T_Lock\Output\fzzl.json'), os.path.getmtime(r'C:\Users\work_space\python\T_Lock\Output\fzzl.json'), os.path.getctime(r'C:\Users\work_space\python\T_Lock\Output\fzzl.json')],
#            [os.path.getatime(r'C:\Users\work_space\python\T_Lock\Output\fzzl.lock'), os.path.getmtime(
#                r'C:\Users\work_space\python\T_Lock\Output\fzzl.lock'), os.path.getctime(r'C:\Users\work_space\python\T_Lock\Output\fzzl.lock')],
#            [os.path.getatime(r'C:\Users\work_space\python\T_Lock\Output\fzzl.zip'), os.path.getmtime(
#                r'C:\Users\work_space\python\T_Lock\Output\fzzl.zip'), os.path.getctime(r'C:\Users\work_space\python\T_Lock\Output\fzzl.zip')],
#            [os.path.getatime(r'C:\Users\work_space\python\T_Lock\Output\fzzl.jpg'), os.path.getmtime(r'C:\Users\work_space\python\T_Lock\Output\fzzl.jpg'), os.path.getctime(r'C:\Users\work_space\python\T_Lock\Output\fzzl.jpg')])
# )

    # json time: [1638405589.124789, 1628218606.0, 1638404836.3001447]
    # lock time: [1638405589.121327, 1628218606.0, 1638404837.6501508]

    # json time: [1638405745.4048784, 1628218606.0, 1638405745.4038806]
    # lock time: [1638405745.4038806, 1628218606.0, 1638405745.381882]

    
    # zip time: [1638405590.145508, 1638405589.124789, 1638405589.1102812]
    # jpg time: [1638405590.1637194, 1638405589.1317966, 1638405589.130836]


print(
    '''
    json time: %s
    lock time: %s

    ''' % ([os.path.getatime(r'C:\Users\work_space\python\T_Lock\Output\fzzl.json'), os.path.getmtime(r'C:\Users\work_space\python\T_Lock\Output\fzzl.json'), os.path.getctime(r'C:\Users\work_space\python\T_Lock\Output\fzzl.json')],
           [os.path.getatime(r'C:\Users\work_space\python\T_Lock\Output\fzzl.lock'), os.path.getmtime(
               r'C:\Users\work_space\python\T_Lock\Output\fzzl.lock'), os.path.getctime(r'C:\Users\work_space\python\T_Lock\Output\fzzl.lock')]
           ))