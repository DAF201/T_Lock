ori = 'helloworld'
ori = " ".join(ori[i:i+2] for i in range(0, len(ori), 2))
ori=ori.split(' ')
print(ori)