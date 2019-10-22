a = 10


def test_global():
    global a
    a = 100
    print("test_global 方法内的 a 值： ", a)


def demo():
    a = 5

    def test_nonlocal():
        nonlocal a
        a = 50
        print("test_nonlocal 方法内的 a 值： ", a)
    test_nonlocal()
    print("demo 方法内的 a 值： ", a)

test_global()
demo()
print("方法外的 a 值： ", a)
