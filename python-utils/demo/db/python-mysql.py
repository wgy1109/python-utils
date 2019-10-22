import MySQLdb


def selectVersion():
    # 查询 数据库版本
    cursor.execute("select VERSION()")
    data = cursor.fetchone()
    print("Database vension : %s " % data)


def create_table():
    # 新建表
    sql = "drop table if exists employee"
    cursor.execute(sql)
    sql = """create table employee (
           first_name char(20) not null,
           last_name char(20),
           age int,
           sex char(1),
           income float ) """
    cursor.execute(sql)


def insert_msg():
    # 插入
    # sql = """ insert into employee ( first_name, last_name, age, sex, income)
    #        value ('Mac','Mohan',20,'M',2000) """

    sql = " insert into employee ( first_name, \
            last_name, age, sex, income ) \
            values (%s, %s, 23, %s, 3000 ) " % ('Wang', 'Yiyi', 'W')
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()


if __name__ == '__main__':
    print('使用 python 连接 mysql ')

    db = MySQLdb.connect("192.168.1.65", "xny", "XNY!qazxsw2", "venusiot", charset='utf8')
    cursor = db.cursor()
    selectVersion()
    db.close()
