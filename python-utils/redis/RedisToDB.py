#!/usr/bin/python3
__author__ = "KF_LIU"
import redis
import psycopg2

pool = redis.ConnectionPool(host='192.168.1.39', port=6379,db=3)
r = redis.Redis(connection_pool=pool)

_myCursor = None
_myDB = None
number = 0

def init():
    global _myCursor
    global _myDB
    global number
    _myDB = psycopg2.connect(
        host='192.168.10.22',
        port='5432',
        database='wisdom',
        user='postgres',
        password='postgres'
    )
    print(_myDB)
    _myCursor = _myDB.cursor()



def InsertResult( deviceid ):
     global _myCursor
     global _myDB
     strSql = "insert into so_device ( sim_num, type, device_name,is_show )\
          values(\'{}\',1,'车',true);".format(deviceid)
     #插入数据
     _myCursor.execute(strSql)
     # 数据表内容有更新，必须使用到该语句
     _myDB.commit()


def Insert( deviceid):
    global _myCursor
    global _myDB
    strSql = "insert into so_device ( sim_num, type, device_name,is_show )\
          values(\'{}\',4,'充电桩站点',true);".format(deviceid)
    # 插入数据
    _myCursor.execute(strSql)
    # 数据表内容有更新，必须使用到该语句
    _myDB.commit()

def Insert2(deviceid):
    global _myCursor
    global _myDB
    strSql = "insert into so_device ( sim_num, type, device_name,is_show )\
          values(\'{}\',2,'充电桩',false);".format(deviceid)
    # 插入数据
    _myCursor.execute(strSql)
    # 数据表内容有更新，必须使用到该语句
    _myDB.commit()

def closeDB():
    global _myCursor
    global _myDB
    _myCursor.close()
    _myDB.close()


def getDevOnlineInfocar():
    strmsg = '02,03,01'
    for key in r.scan_iter(match='jVcnIMCb3Xf*1002900', count=1000):
        strkey = str(key, encoding='utf-8')
        datatype = strkey[12:14]
        if(strmsg.find(datatype) >= 0 ):
            continue
        deviceid = strkey[12:24]
        if ("00".find(datatype) >= 0):
            InsertResult(deviceid)
            continue

        if ("10".find(datatype) >= 0):
            Insert(deviceid)
            continue

        if ("20".find(datatype) >= 0):
            Insert2(deviceid)
            continue

init()
getDevOnlineInfocar()
closeDB()
