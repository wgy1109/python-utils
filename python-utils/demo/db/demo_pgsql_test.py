# -*- coding:utf-8 -*-
import psycopg2

mydb = psycopg2.connect(
    host='127.0.0.1',
    port='5432',
    database='test',
    user='postgres',
    password='root'
)

print(mydb)
mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM student LIMIT 10")
rows = mycursor.fetchall()
print(rows)
mydb.commit()


def test_ctreatdb():
    # 创建表
    # mycursor.execute('create table student(id serial primary key,student_name varchar(20),age int ,class_name varchar(20));')
    # 插入数据
    mycursor.execute("insert into student (student_name,age,class_name) values('s1',18,'class1');\
    insert into student (student_name,age,class_name) values('s2',22,'class1');\
    insert into student (student_name,age,class_name) values('s3',18,'class2');")
    # 查询并打印(读取Retrieve)
    mycursor.execute("select * from student")
    rows = mycursor.fetchall()
    print('--------------------------------------------------------------------------------------')
    for row in rows:
        print(
            'id=' + str(row[0]) + ' student_name=' + str(row[1]) + ' age=' + str(row[2]) + ' class_name=' + str(row[3]))
        print('--------------------------------------------------------------------------------------\n')

    # mycursor.execute("ALTER TABLE sites ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY")
    # mycursor.execute("CREATE TABLE sites2 (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), url VARCHAR(255))")
    # sql = "INSERT INTO sites (name, url) VALUES (%s, %s)"
    # val = ("RUNOOB", "https://www.runoob.com")
    # mycursor.execute(sql, val)
    # 数据表内容有更新，必须使用到该语句
    mydb.commit()

    print(mycursor.rowcount, "记录插入成功。")


'''
mycursor.execute("SHOW DATABASES")
 
for x in mycursor:
  print(x)
'''


# 向 sites 表插入一条记录。
def test_insert():
    # 创建表
    mycursor.execute('create table sites(id serial primary key,name varchar(80), url varchar(80));')

    sql = "INSERT INTO sites (name, url) VALUES (%s, %s)"
    val = ("RUNOOB", "https://www.runoob.com")

    mycursor.execute(sql, val)
    mydb.commit()  # 数据表内容有更新，必须使用到该语句
    print(mycursor.rowcount, "记录插入成功。")


# 批量插入
# 批量插入使用 executemany() 方法，该方法的第二个参数是一个元组列表，包含了我们要插入的数据：
def test_insertmany():
    sql = "INSERT INTO sites (name, url) VALUES (%s, %s)"
    val = [
        ('Google', 'https://www.google.com'),
        ('Github', 'https://www.github.com'),
        ('Taobao', 'https://www.taobao.com'),
        ('stackoverflow', 'https://www.stackoverflow.com/')
    ]

    mycursor.executemany(sql, val)
    mydb.commit()  # 数据表内容有更新，必须使用到该语句
    print(mycursor.rowcount, "记录插入成功。")


# DESC 按 name 字段字母的降序排序：
def test_desc():
    sql = "SELECT * FROM sites ORDER BY name DESC"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    for x in myresult:
        print(x)

    # LIMIT 读取前 3 条记录


def test_limit():
    mycursor.execute("SELECT * FROM sites LIMIT 3")
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)


# 从第二条开始读取前 3 条记录
def test_offset():
    mycursor.execute("SELECT * FROM sites LIMIT 3 OFFSET 1")  # 0 为 第一条，1 为第二条，以此类推
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)


# 删除记录
'''
注意：要慎重使用删除语句，删除语句要确保指定了 WHERE 条件语句，否则会导致整表数据被删除。

'''


def test_delete():
    sql = "DELETE FROM sites WHERE name = 'stackoverflow'"
    # 为了防止数据库查询发生 SQL 注入的攻击，我们可以使用 %s 占位符来转义删除语句的条件：
    sql = "DELETE FROM sites WHERE name = %s"
    na = ("stackoverflow",)

    mycursor.execute(sql)
    mydb.commit()
    print(mycursor.rowcount, " 条记录删除")


# 更新表数据
def test_update():
    sql = "UPDATE sites SET name = %s WHERE name = %s"
    val = ("Zhihu", "ZH")

    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, " 条记录被修改")


# 删除表
def test_deltable():
    sql = "DROP TABLE IF EXISTS sites"  # 删除数据表 sites

    mycursor.execute(sql)


# test_ctreatdb()
# test_insert()
# test_insertmany()
test_desc()
test_limit()
test_offset()
mycursor.close()
mydb.close()
