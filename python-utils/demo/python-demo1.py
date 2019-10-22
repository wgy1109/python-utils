import time;


def getage(name):
    if name == "小张":
        print('小张')
        return 18;
    elif "小李" == name:
        print('小李')
        return 24;
    else:
        print('没人，返回默认的 16')
        return 16;


if __name__ == '__main__':
    print('hello')
    print('name %s ,age %d !' % ('aaa', 32))
    dict = {'a': 1, 'b': 2, 'b': 3}
    print(dict)
    dict['b'] = 8
    print(dict)
    dict['c'] = 22
    print(dict)
    print('当前时间戳： ', time.time())
    print('本地时间为： ', time.localtime(time.time()))
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    print(getage('小'));
    print("--------------------------割---------------")
    # str = input("请输入：")
    # print("你输入的是：", str)

    try:
        fh = open("testfile", "w")
        try:
            fh.write("测试文件，测试异常！！")
        finally:
            print("关文件")
            fh.close()
    except IOError:
        print("Error : 没找到文件，读取失败！")
