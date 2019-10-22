#  python 2 使用 thread， python 3 使用了 _thread
#  调用 thread 模块中的 start_new_thread() 函数来产生新线程
import _thread
import time

def print_time(threadName, delay):
    count = 0
    while count < 5:
        time.sleep(delay)
        count += 1
        # print "%s : %s" % (threadName, time.ctime(time.time()))
        print(threadName+" -- "+time.ctime(time.time()))

try:
    _thread.start_new_thread( print_time, ("thread-1", 2, ))
    _thread.start_new_thread( print_time, ("thread-2", 4, ))
except:
    print("error : start error")

while 1:
    pass