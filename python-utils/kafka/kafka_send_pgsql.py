# -*- coding:UTF-8 -*-
from kafka import KafkaConsumer
import time
import psycopg2

# 默认初始化 pgsql 连接
mydb = psycopg2.connect(
    host='192.168.10.22',
    port='5432',
    database='iot',
    user='postgres',
    password='postgres'
)


# 日志打印
def log(str):
    t = time.strftime(r"%Y-%m-%d %H:%M:%S", time.localtime())
    print("[%s] %s"%(t, str))


# 获取 kafka 数据
def get_kafka_msg():
    consumer = KafkaConsumer('shadow_data_topic12', group_id='group_sdt_py_save_pgsql', bootstrap_servers=["192.168.1.6:9092","192.168.1.7:9092","192.168.1.8:9092"])
    insert_num = 0
    # msg1 = ('6', 'c9XeFSPGmbo')
    # msg2 = ('7', 'WxkJfmutLLs')
    # msg3 = ('8', '0MRyfGQQw65')
    # val=[]
    # val.append(msg1)
    # val.append(msg2)
    # val.append(msg3)
    # print(val)
    #
    # val.clear()
    # print(val)
    val = []
    for msg in consumer:
        if msg is not None:
            insert_num += 1
            recv = "%s:%d:%d: key=%s value=%s" %(msg.topic, msg.partition, msg.offset, str(msg.key, encoding='utf-8'),  msg.value)
            log(recv)
    #         msg1 = (insert_num, 'c9XeFSPGmbo')
    #         val.append(msg1)
    #         if(insert_num % 3 == 0):
    #             table_insert(val)
    #             val.clear()
    #
    # if(len(val) > 0):
    #     table_insert(val)
    #     val.clear()
    # log("本次循环插入数据量： %s" % ( str(insert_num) ))


sql = "INSERT INTO statistical_data ( id, pk ) VALUES  ( %s, %s )"
def table_insert(val):
    global sql
    # sql = "INSERT INTO xny_table ( device_id, collect_time, data_type, on_line, device_type, product_key, date_time, message_id, alarm, sim_num, version, api_key, body ) VALUES  ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )"

    mycursor.executemany(sql, val)
    mydb.commit()  # 数据表内容有更新，必须使用到该语句
    print(mycursor.rowcount, "记录插入成功。")

# 主方法 用于启动
if __name__ == '__main__':

    # print(mydb)
    # mycursor = mydb.cursor()
    get_kafka_msg()

    # msg1 = ('6', 'c9XeFSPGmbo')
    # msg2 = ('7', 'WxkJfmutLLs')
    # msg3 = ('8', '0MRyfGQQw65')
    # val=[]
    # val.append(msg1)
    # val.append(msg2)
    # val.append(msg3)
    # print(val)
    #
    # val.clear()
    # print(val)

    #
    # table_insert(val)
    # mycursor.execute("SELECT * FROM xny_table LIMIT 10")
    # rows = mycursor.fetchall()
    # print(rows)
    # mydb.commit()

    # mycursor.close()
    # mydb.close()
