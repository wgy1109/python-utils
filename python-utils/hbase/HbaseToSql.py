#!/usr/bin/python3
__author__ = "NIU"

import happybase as hb
import redis
import time
import psycopg2

pool = redis.ConnectionPool(host='192.168.1.39', port=6379, db=3)
r = redis.Redis(connection_pool=pool)


def printTime():
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))


def getDevOnlineInfocar():
    count = 0
    dataList = []
    for key in r.scan_iter(match='*', count=1000):
        strkey = str(key, encoding='utf-8')
        if len(strkey) > 26:
            dataList.append(strkey)
            count = count + 1
    print("从 redis 取到的key ： ", count)
    return dataList


class myHbase:





    def __init__(self):
        self.myConnect = hb.Connection('192.168.1.20',9090)
        self.myTable = self.myConnect.table('xny_data_hbase')

    def queryByTime(self):
        count_rowList = 0
        strSql = "insert into xny_hbase (data_inteval, data_type_str, alarm, device_id, sim_num, lac, sn, collect_time, cellid, collection_time," \
                 "data_type, cur_map_type, on_line, device_type, direction, version, product_key, devid_str, latitude, message_id, date_time, longitude, " \
                 "body, mnc, dev_type_str ) values "

        print("开始获取redis 数据 ： ", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        redisData=getDevOnlineInfocar()
        redisData = sorted(redisData)
        print("获取redis 数据 结束，开始循环redis key  ", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

        for strkey in redisData:
            print(time.strftime('%Y-%m-%d %H:%M:%S',  time.localtime(time.time())), strkey , count_rowList)
            pk = strkey[0:11]
            devids = strkey[12:24]
            datatype = strkey[25:32]
            devid = devids[::-1]
            start_row = bytes('{}{}{}{}'.format(devid, pk, datatype, "1568782800000"), encoding='utf-8')
            stop_row = bytes('{}{}{}{}'.format(devid, pk, datatype, "1568783400000"), encoding='utf-8')
            rowList = self.myTable.scan(row_start=start_row, row_stop=stop_row)
            if (rowList == None):
                return

            for k, v in rowList:
                count_rowList += 1
                dataInteval = ""
                if str(v).find("b'f:dataInteval'") != -1 :
                    dataInteval = str(v[b'f:dataInteval'], encoding='utf-8')
                dataTypeStr = str(v[b'f:dataTypeStr'], encoding='utf-8')
                alarm = str(v[b'f:alarm'], encoding='utf-8')
                deviceId = str(v[b'f:deviceId'], encoding='utf-8')
                simNum = str(v[b'f:simNum'], encoding='utf-8')
                if simNum == '':
                    simNum = ''
                lac = str(v[b'f:lac'], encoding='utf-8')
                sn = str(v[b'f:sn'], encoding='utf-8')
                collectTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                if str(v).find("b'f:collectTime'") != -1:
                    collectTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(str(v[b'f:collectTime'], encoding='utf-8')) / 1000))
                cellid = str(v[b'f:cellid'], encoding='utf-8')
                collectionTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(str(v[b'f:collectionTime'], encoding='utf-8')) / 1000))
                dataType = str(v[b'f:dataType'], encoding='utf-8')
                curMapType = str(v[b'f:curMapType'], encoding='utf-8')
                onLine = int(v[b'f:onLine'])
                deviceType = str(v[b'f:deviceType'], encoding='utf-8')
                direction = str(v[b'f:direction'], encoding='utf-8')
                version = str(v[b'f:version'], encoding='utf-8')
                productKey = str(v[b'f:productKey'], encoding='utf-8')
                devidStr = str(v[b'f:devidStr'], encoding='utf-8')
                latitude = str(v[b'f:latitude'], encoding='utf-8')
                messageId = str(v[b'f:messageId'], encoding='utf-8')
                if messageId == '':
                    messageId = 0
                dateTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(str(v[b'f:dateTime'], encoding='utf-8')) / 1000))
                longitude = str(v[b'f:longitude'], encoding='utf-8')
                body = str(v[b'f:body'], encoding='utf-8')
                mnc = str(v[b'f:mnc'], encoding='utf-8')
                devTypeStr = str(v[b'f:devTypeStr'], encoding='utf-8')
                str_sql = "(\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\'),".format(
                    dataInteval, dataTypeStr, alarm, deviceId, simNum, lac, sn, collectTime, cellid, collectionTime,
                    dataType, curMapType, onLine, deviceType, direction, version, productKey, devidStr, latitude, messageId,
                    dateTime, longitude, body, mnc, devTypeStr )
                strSql = strSql + str_sql

                if count_rowList % 100 == 0:
                    print(time.strftime('%Y-%m-%d %H:%M:%S',  time.localtime(time.time())), count_rowList,   strSql[:len(strSql)-1])
                    _pgDB.InsertResultBystr(strSql[:len(strSql)-1])
                    strSql = "insert into xny_hbase (data_inteval, data_type_str, alarm, device_id, sim_num, lac, sn, collect_time, cellid, collection_time," \
                             "data_type, cur_map_type, on_line, device_type, direction, version, product_key, devid_str, latitude, message_id, date_time, longitude, " \
                             "body, mnc, dev_type_str ) values "

        print(time.strftime('%Y-%m-%d %H:%M:%S',    time.localtime(time.time())), count_rowList,  strSql[:len(strSql) - 1])
        _pgDB.InsertResultBystr(strSql[:len(strSql)-1])
        print("循环redis key结束  ： ", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

class PersonDeviceRest:

    def __init__(self):
        self._myCursor = None
        self._myDB = None

    def init(self):
        self._myCursor = None
        self._myDB = None
        self.number = 0
        self._myDB = psycopg2.connect(
            host='localhost',
            port='5432',
            database='test',
            user='postgres',
            password='root'
        )
        print(self._myDB)
        self._myCursor = self._myDB.cursor()


    def InsertResultBystr(self, strSql):
        # 插入数据
        try:
            self._myCursor.execute(strSql)
            # 数据表内容有更新，必须使用到该语句
            self._myDB.commit()
        except psycopg2.Error as e:
            print(e.pgerror)
            print(e.diag.message_detail)
            self._myDB.commit()
            self.number = self.number + 1
            print('主键冲突个数：{}', self.number)

    def closeDB(self):
        self._myCursor.close()
        self._myDB.close()


if __name__ == '__main__':
    global _pgDB
    _pgDB = PersonDeviceRest()
    _pgDB.init()
    myhbase = myHbase()
    myhbase.queryByTime()