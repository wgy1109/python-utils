import re


# 父类子类继承关系
class Parent:  # 定义父类
    def myMethod(self):
        print('调用父类方法')


class Child(Parent):  # 定义子类
    def myMethod(self):
        print('调用子类方法')


# 类的私有方法
class JustCounter:
    __secretCount = 0  # 私有变量
    publicCount = 0  # 公开变量

    def count(self):
        self.__secretCount += 1
        self.publicCount += 1
        print
        self.__secretCount


if __name__ == "__main__":
    print("demo 2 begin ")
    # 父子类
    c = Child()  # 子类实例
    c.myMethod()  # 子类调用重写方法

    # 类的私有方法调用
    counter = JustCounter()
    counter.count()
    counter.count()
    print(counter.publicCount)
    # print(counter.__secretCount)  # 报错，实例不能访问私有变量
    # 通过  object._className__attrName（ 对象名._类名__私有属性名 ）访问私有属性
    print(counter._JustCounter__secretCount)

    # 正则表达式
    # re.match 尝试从字符串的起始位置匹配一个模式，没有匹配成功返回none
    print(re.match('www', 'www.runoob.com').span())  # 在起始位置匹配
    print(re.match('com', 'www.runoob.com'))  # 不在起始位置匹配

    line = "Cats are smarter than dogs"

    matchObj = re.match(r'(.*) are (.*?) .*', line, re.M | re.I)

    if matchObj:
        print("matchObj.group() : ", matchObj.group())
        print("matchObj.group(1) : ", matchObj.group(1))
        print("matchObj.group(2) : ", matchObj.group(2))
    else:
        print("No match!!")

    # re.search 扫描整个字符串,并返回第一个成功的匹配
    print(re.search('com', 'www.runoob.com').span())  # 不在起始位置匹配

    # re.sub 检索和替换 用于替换字符串中的匹配项
    phone = "2004-959-559 # 这是一个国外电话号码"
    # 删除字符串中的 Python注释
    num = re.sub(r'#.*$', "", phone)
    print("电话号码是: ", num)
    # 删除非数字(-)的字符串
    num = re.sub(r'\D', "", phone)
    print("电话号码是 : ", num)


    # 将匹配的数字乘以 2
    def double(matched):
        value = int(matched.group('value'))
        return str(value * 2)


    s = 'A23G4HFD567'
    print(re.sub('(?P<value>\d+)', double, s))

    pattern = re.compile(r'\d+')  # 用于匹配至少一个数字
    m = pattern.match('one12twothree34four')  # 查找头部，没有匹配
    print("查找头部，没有匹配 : ", m)
    m = pattern.match('one12twothree34four', 2, 10)  # 从'e'的位置开始匹配，没有匹配
    print("从'e'的位置开始匹配，没有匹配 : ", m)
    m = pattern.match('one12twothree34four', 3, 10)  # 从'1'的位置开始匹配，正好匹配
    print("从'1'的位置开始匹配，正好匹配 : ", m)
    m.group(0)  # 可省略 0
    m.start(0)  # 可省略 0

    # 查找字符串中所有数字
    pattern = re.compile(r'\d+')  # 查找数字
    result1 = pattern.findall('runoob 123 google 456')
    result2 = pattern.findall('run88oob123google456', 0, 10)
    print(result1)
    print(result2)

    # 在字符串中找到正则表达式所匹配的所有子串，并把它们作为一个迭代器返回。
    it = re.finditer(r"\d+", "12a32bc43jf3")
    for match in it:
        print(match.group())

    # split 方法按照能够匹配的子串将字符串分割后返回列表，它的使用形式如下：
    print(re.split(r'\W+', 'runoob, runoob, runoob'))
    print(re.split(r'(\W+)', ' runoob, runoob, runoob.'))
    print(re.split(r'\W+', ' runoob, runoob, runoob.', 1))
    # print(re.split('a*', 'hello world'))  # 对于一个找不到匹配的字符串而言，split 不会对其作出分割
