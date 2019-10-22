import os
import time

path1 = 'D:/Code/svnPyCharm/pythonTest/logs.txt'
file = open(path1, 'r')

for line in file:
    str=line.split()[3]
    otime=str[1:12]
    print("otime, {}", otime)
    time_jieshu = time.strptime(otime, '%Y-%m-%d')
    time_jieshu = int(time.mktime(time_jieshu))
    ntime=time.strftime('%Y-%m-%d',time.localtime(time_jieshu))
    #  print ntime

    log_file='/lianxi/python/split/access.log-%s' %ntime

    with open(log_file,'a') as f:
        if not os.path.exists(log_file):
            os.mknod(log_file)
    #      f.write(line)
    #    else:
        f.write(line)
        f.close()