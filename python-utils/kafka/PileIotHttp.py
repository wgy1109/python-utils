# -*- coding:UTF-8 -*-
from apscheduler.schedulers.blocking import BlockingScheduler

__author__ = "NIU"
import base64
import datetime
import re
import urllib
from flask import logging
from kafka.errors import KafkaError
import requests
import json
import time
import logging
from kafka import KafkaProducer

LOGURL = 'D:/Code/svnPyCharm/pythonTest/'
# LOGURL = '/home/clouduser/service/python/pileAndCar/logs/'
# LOGURL = '../logs/'

producer = KafkaProducer(bootstrap_servers=["192.168.1.6:9092", "192.168.1.7:9092", "192.168.1.8:9092"])

def initLogging():
    fmt = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s'
    today = datetime.date.today()
    filenameurl = '{}logs-{}.log'.format(LOGURL, str(today))
    print("filenameurl: ", filenameurl)
    logging.basicConfig(
        level=logging.INFO,
        format=fmt,
        filename=filenameurl,
        filemode='a',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('LINE %(lineno)-4d : %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)


def formatKafka(
        deviceId="",
        body=None
):
    res = dict()
    redisDict = dict()
    # redisDict["deviceId"] = '{}{}'.format(code, siteCode)
    redisDict["deviceId"] = deviceId
    redisDict["deviceType"] = "4010304030602#车站点"
    redisDict["apiKey"] = "A4026FD47174E543EA41C538A8B430C6"
    redisDict["productKey"] = "jVcnIMCb3Xf"
    redisDict["dateTime"] = str(int(round(time.time() * 1000)))
    redisDict["curMapType"] = ""
    redisDict["longitude"] = ""
    redisDict["latitude"] = ""
    redisDict["direction"] = ""
    redisDict["mnc"] = ""
    redisDict["lac"] = ""
    redisDict["cellid"] = ""
    redisDict["messageId"] = ""
    redisDict["dataType"] = "1002900"
    redisDict["onLine"] = "1"
    redisDict["alarm"] = ""
    redisDict["simNum"] = ""
    redisDict["version"] = ""
    bytesStr = str(body).replace("\'", "\"").encode(encoding='utf-8')
    string = str(bytesStr, 'utf-8')
    partten = re.sub('None', '\"None\"', string)
    part = re.sub('False', '\"False\"', partten)
    partt = re.sub('True', '\"True\"', part)
    b = bytes(partt, encoding='utf-8')
    b64str = base64.b64encode(b)
    redisDict["body"] = b64str.decode()
    ret = bytes('{}'.format(str(redisDict).replace("\'", "\"")), 'utf-8')
    logging.info("数据发送kafka 参数信息 {} ".format(ret))
    return ret


def sendmsg(bmsg, bkey):
    result = producer.send("router2shadow_jVcnIMCb3Xf", value=bmsg, key=bkey)
    try:
        _ = result.get(timeout=10)
    except KafkaError as kerr:
        print(kerr)
    logging.info("数据发送kafka成功 参数信息 {} ".format(result))



# 查询站点接口
def getstatus():
    url = 'http://localhost/api_cloud/api/ebc/hw/siteListByNameV2'
    body = {"siteName": "丹迪酒店茶楼（前坪停车场）", "siteType": "3"}
    headers = {'content-type': "application/json"}
    # print type(json.dumps(body))
    # 这里有个细节，如果body需要json形式的话，需要做处理
    # 可以是data = json.dumps(body)
    response = requests.post(url, data=json.dumps(body), headers=headers)
    retdata = response.text
    iot_d = json.loads(retdata)
    dataList = iot_d["data"]
    for body in dataList:
        siteId = body["siteId"]
        # getEquipment(siteId)
        siteCode = body["siteCode"]
        code = "10"
        deviceId = '{0}{1}'.format(code, siteCode)
        msg = formatKafka(deviceId, body)
        b = bytes(deviceId, encoding='utf-8')
        # sendmsg(msg, b)
        sendmsg(b'2', b'3')



# 根据站点查询站点对应设备的明细接口
def getEquipment(siteId=None):
    url = 'http://localhost/api_cloud/api/ebc/hw/parkToEqpTypeV2'
    siteIds = '9835b6eabc774b83b5a84aea8c8776a0'
    # siteIds=siteId
    geturl = '{0}/{1}'.format(url, siteIds)
    resu = urllib.request.urlopen(geturl, data=None, timeout=10)
    retdata = resu.read().decode()
    iot_d = json.loads(retdata)
    ret = iot_d["data"]
    eqpPile = ret["parkToEqpList"]
    for body in eqpPile:
        eqpPileId = body["eqpPileId"]
        if (eqpPileId == None):
            continue
        deviceI = eqpPileId[3:14]
        code = "20"
        deviceId = '{0}{1}'.format(code, deviceI)
        msg = formatKafka(deviceId, body)
        b = bytes(deviceId, encoding='utf-8')
        sendmsg(msg, b)

# 车辆全部列表
def getCar0List():
    url = 'http://localhost/api_cloud/api/rent/hw/getCarInfoPage'
    carUseStatus = 0
    pageNum = 1
    pageSize = 900
    # carUseStatus为空 传车辆状态信息 为0 租用车辆的使用信息
    geturlT = '{0}?pageNum={1}&pageSize={2}&carUseStatus={3}&carNum='.format(url, pageNum, pageSize, carUseStatus)
    resuN = urllib.request.urlopen(geturlT, data=None, timeout=10)
    ret = resuN.read().decode()
    iot_r = json.loads(ret)
    if(iot_r["code"]==-11):
        return
    ren = iot_r["data"]
    dataN = ren["list"]
    for dataLl in dataN:
        carStatu = dataLl["carStatus"]
        dataLl['latitude'] = carStatu['lat']
        dataLl['longitude'] = carStatu['lng']
        carStatus = carStatu["id"]
        if (len(carStatus) == 6):
            deviceSN = carStatus[0:7]
            # 租用车辆的使用信息
            num = '002000'
            deviceId = '{0}{1}'.format(num, deviceSN)
            msg = formatKafka(deviceId, dataLl)
            b = bytes(deviceId, encoding='utf-8')
            sendmsg(msg, b)
            insertSql(deviceId)
        if (len(carStatus) == 10):
            deviceSN = carStatus[1:10]
            # 租用车辆的使用信息
            num = '002'
            deviceId = '{0}{1}'.format(num, deviceSN)
            msg = formatKafka(deviceId, dataLl)
            b = bytes(deviceId, encoding='utf-8')
            sendmsg(msg, b)
            insertSql(deviceId)
        if(len(carStatus) == 12):
            deviceSN = carStatus[3:13]
            # 租用车辆的使用信息
            num = '002'
            deviceId = '{0}{1}'.format(num, deviceSN)
            msg = formatKafka(deviceId, dataLl)
            b = bytes(deviceId, encoding='utf-8')
            sendmsg(msg, b)
            insertSql(deviceId)
        if (len(carStatus) == 14):
            deviceSN = carStatus[5:15]
            # 租用车辆的使用信息
            num = '002'
            deviceId = '{0}{1}'.format(num, deviceSN)
            msg = formatKafka(deviceId, dataLl)
            b = bytes(deviceId, encoding='utf-8')
            sendmsg(msg, b)
            insertSql(deviceId)

# 车辆租用列表
def getCarList():
    url = 'http://localhost/api_cloud/api/rent/hw/getCarInfoPage'
    carUseStatus = 0
    pageNum = 1
    pageSize = 900
    # carUseStatus为空 传车辆状态信息 为0 租用车辆的使用信息
    geturl = '{0}?pageNum={1}&pageSize={2}&carUseStatus=&carNum='.format(url, pageNum, pageSize)
    resu = urllib.request.urlopen(geturl, data=None, timeout=10)
    retdata = resu.read().decode()
    iot_d = json.loads(retdata)
    if (iot_d["code"] == -11):
        return
    ret = iot_d["data"]
    dataL = ret["list"]
    for dataList in dataL:
        carStatu = dataList["carStatus"]
        dataList['latitude'] = carStatu['lat']
        dataList['longitude'] = carStatu['lng']
        carStatus = carStatu["id"]
        if (len(carStatus) == 6):
            deviceSN = carStatus[0:7]
            # 租用车辆的使用信息
            num = '001000'
            deviceId = '{0}{1}'.format(num, deviceSN)
            msg = formatKafka(deviceId, dataList)
            b = bytes(deviceId, encoding='utf-8')
            sendmsg(msg, b)
            insertSql(deviceId)
        if (len(carStatus) == 10):
            deviceSN = carStatus[1:10]
            # 租用车辆的使用信息
            num = '001'
            deviceId = '{0}{1}'.format(num, deviceSN)
            msg = formatKafka(deviceId, dataList)
            b = bytes(deviceId, encoding='utf-8')
            sendmsg(msg, b)
            insertSql(deviceId)
        if (len(carStatus) == 12):
            deviceSN = carStatus[3:13]
            # 租用车辆的使用信息
            num = '001'
            deviceId = '{0}{1}'.format(num, deviceSN)
            msg = formatKafka(deviceId, dataList)
            b = bytes(deviceId, encoding='utf-8')
            sendmsg(msg, b)
            insertSql(deviceId)
        if (len(carStatus) == 14):
            deviceSN = carStatus[5:15]
            # 所有车辆的状态信息
            num = '001'
            deviceId = '{0}{1}'.format(num, deviceSN)
            msg = formatKafka(deviceId, dataList)
            b = bytes(deviceId, encoding='utf-8')
            sendmsg(msg, b)
            insertSql(deviceId)

# 全量车辆及站点接口
def getCarListAll():
    url = 'http://localhost/api_cloud/api/rent/hw/getAllSitesAndCarInfo'
    resu = urllib.request.urlopen(url, data=None, timeout=10)
    retdata = resu.read().decode()
    if (retdata == '{"code":-11,"msg":"required login "}'):
        return
    iot_d = json.loads(retdata)
    ret = iot_d["data"]
    # 获取车辆信息
    dataL = ret["carMonitorDtoList"]
    for dataList in dataL:
        carStatus = dataList["carId"]
        deviceSN = carStatus[1:11]
        # 01为车辆信息
        num = '01'
        deviceId = '{0}{1}'.format(num, deviceSN)
        msg = formatKafka(deviceId, dataList)
        b = bytes(deviceId, encoding='utf-8')
        sendmsg(msg, b)
    # 获取站点信息
    dataLb = ret["siteAndCar"]
    for dataList in dataLb:
        carStatus = dataList["id"]
        deviceSN = carStatus[1:11]
        # 02为站点信息
        num = '02'
        deviceId = '{0}{1}'.format(num, deviceSN)
        siteId = dataList["id"]
        # getCarSit(siteId)
        msg = formatKafka(deviceId, dataList)
        b = bytes(deviceId, encoding='utf-8')
        sendmsg(msg, b)
        insertSql(deviceId)

# 车辆站点明细接口
def getCarSit(siteId=None):
    url = 'http://localhost/api_cloud/api/rent/hw/siteInfoById'
    siteIds = '1c9dd03dc8c14e4fb5b02897ec0a6c83'
    # siteIds=siteId
    geturl = '{0}?siteId={1}'.format(url, siteIds)
    resu = urllib.request.urlopen(geturl, data=None, timeout=10)
    retdata = resu.read().decode()
    iot_d = json.loads(retdata)
    ret = iot_d["data"]
    ret['msgType'] = "0"
    eqpPileId = ret["id"]
    if (eqpPileId == None):
        return
    deviceSN = eqpPileId[0:10]
    # 站点明细
    num = '03'
    deviceId = '{0}{1}'.format(num, deviceSN)
    msg = formatKafka(deviceId, ret)
    b = bytes(deviceId, encoding='utf-8')
    sendmsg(msg, b)

# 将定时任务存到数据库
def insertSql(deviceId):
    url = 'http://192.168.2.13:80/code/product.do?add'
    body = {"devName": "车辆状态信息", "devType": "C01C01C01", "devNewId": deviceId, "devOldId": "",
            "orgid": "1001"}
    headers = {'content-type': "application/json"}
    response = requests.post(url, data=json.dumps(body), headers=headers)
    retdata = response.text
    logging.info("deviceId 添加数据库成功  ".format(retdata))

# 定时任务
def myscheduler():
    # 创建后台执行的 schedulers
    scheduler = BlockingScheduler()
    # 添加调度任务
    # 调度方法为 timedTask，触发器选择 interval(间隔性)，间隔时长为 90 秒
    # scheduler.add_job(method, 'interval', seconds=300)
#    scheduler.add_job(getstatus, 'interval', seconds=90)
#    scheduler.add_job(getEquipment, 'interval', seconds=90)
    scheduler.add_job(getCarList, 'interval', seconds=3)
    scheduler.add_job(getCar0List, 'interval', seconds=3)
#    scheduler.add_job(getCarListAll, 'interval', seconds=300)
#    scheduler.add_job(getCarSit, 'interval', seconds=90)
    # 启动调度任务
    scheduler.start()

# # def method():
# #     # # 查询站点接口
# # getstatus()
#
# # getEquipment()
# #     # #车辆列表
# getCarList()
# #     #全量车辆及站点接口
# # getCarListAll()
# # getCarSit()
# # sendmsg(b'1', b'2')
# 初始化日志信息
initLogging()
# 定时任务
myscheduler()
producer.flush()
producer.close()

