# -*- coding:utf-8 -*-
import psycopg2


class myPgDB:

    def __init__(self, name, connection):
        self._myCursor = None
        self._myDB = None

    def init(self):
        self._myCursor = None
        self._myDB = None
        self._myDB = psycopg2.connect(
            host='127.0.0.1',
            port='5432',
            database='test',
            user='postgres',
            password='root'
        )
        print(self._myDB)
        self._myCursor = self._myDB.cursor()

    def test_insert(self):
        # 插入数据

        self._myCursor.execute("insert into personiotstatistics (date,gpsNum,msgNum,TotalLen) values('2019-6-30',18,20,30.5);\
        insert into personiotstatistics (date,gpsNum,msgNum,TotalLen) values('2019-6-30',18,20,30.5);\
          insert into personiotstatistics (date,gpsNum,msgNum,TotalLen) values('2019-6-30',18,20,30.5);")

        # 数据表内容有更新，必须使用到该语句
        self._myDB.commit()

    def InsertResult(self,
                     date=None,
                     msgNum=-1,
                     gpsNum=-1,
                     TotalLen=0.0
                     ):
        strSql = "insert into PersonIotStatistics (date,gpsNum,msgNum,TotalLen)\
          values(\'{}\',{},{},{});".format(date, msgNum, gpsNum, TotalLen)

        # 插入数据
        self._myCursor.execute(strSql)
        # 数据表内容有更新，必须使用到该语句
        self._myDB.commit()

    def closeDB(self):
        self._myCursor.close()
        self._myDB.close()
