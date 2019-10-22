#!/usr/bin/python3
__author__ = "KF_LIU"
import redis

pool = redis.ConnectionPool(host='192.168.1.39', port=6379,db=3)
r = redis.Redis(connection_pool=pool)

def getDevOnlineInfocar():
    strmsg = '1000001,1000101,1000200,1000301,1000401,1000505,1001801,1001901,1002104,1002500,1002701,1002800'
    for key in r.scan_iter(match='*', count=1000):
        strkey = str(key, encoding='utf-8')
        datatype = strkey[-7:]
        if(strmsg.find(datatype) == -1 or datatype == '' or datatype == '1' ):
            continue
        t = r.hgetall(strkey)
        print(t)
        strmsg = strmsg.replace(datatype, "")

getDevOnlineInfocar()

