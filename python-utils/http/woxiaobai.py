# -*- coding:UTF-8 -*-
import requests
import json
import time
import base64
import logging
import datetime
from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import KafkaError
from apscheduler.schedulers.background import BlockingScheduler
from requests_toolbelt import MultipartEncoder


_BASE_URL = 'http://localhost/wobida/carStatus?vin='
VIN = ['IDPWXB201001930021']
AUTHORIZATION = 'bearer '
TOKEN = 'cdab658f-4baf-4e6a-bcc1-91b5a777bd39'
APIKEY = 'A4026FD47174E543EA41C538A8B430C6'
PRODUCTKEY = 'jVcnIMCb3Xf'
DATATYPE = '1002900'
TOPIC = 'router2shadow_jVcnIMCb3Xf'

GETTOKENURL = 'http://localhost/api-auth/oauth/token'
USERNAME = 'user'
PASSWORD = 'pwd'
GRANT_TYPE = 'password'
CLIENT_ID = 'client_id'
CLIENT_SECRET = 'client_secret'
SCOPE = 'all'
# LOGURL = 'D:/Code/svnPyCharm/pythonTest/'
LOGURL = '/home/clouduser/service/python/woxiaobai/logs/'

producer = KafkaProducer(bootstrap_servers=["192.168.1.6:9092","192.168.1.7:9092","192.168.1.8:9092"])


def initLogging():
    fmt = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s'
    today = datetime.date.today()
    filenameurl = '{}logs-{}.log'.format(LOGURL,str(today))
    print("filenameurl: ",filenameurl)
    logging.basicConfig(
                        level=logging.INFO,
                        format=fmt,
                        filename=filenameurl,
                        filemode='a',
                        datefmt='%Y-%m-%d %H:%M:%S'
                        )
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('LINE %(lineno)-4d : %(levelname)-8s %(message)s');
    console.setFormatter(formatter);
    logging.getLogger('').addHandler(console);


# 初始化日志信息
initLogging()


def getToken():
    global TOKEN
    body = MultipartEncoder(
        fields={
            "username": (None, USERNAME),
            "password": (None, PASSWORD),
            "grant_type": (None, GRANT_TYPE),
            "client_id": (None, CLIENT_ID),
            "client_secret": (None, CLIENT_SECRET),
            "scope": (None, SCOPE)
            })
    response = requests.post(GETTOKENURL, data=body, timeout=10, verify=False, headers={'Content-Type': body.content_type})
    TOKEN = json.loads(str(response.text))['access_token']
    logging.info("获取token 得到信息 {} ".format(response.text))


def getSiteList(
        url=""
):
    headers={"Authorization":AUTHORIZATION+TOKEN}
    result = requests.get(url=url, headers=headers).text
    if result == "":
        getToken()
        return ""
    result = json.loads(result)
    code = result['code']
    if "200" != str(code):
        logging.error("调用url - {}返回错误， code - {} ".format(url, code))
        return ""
    data = result['data']
    is_login = data['is_login']
    data['msgType'] = "0"
    if(is_login):
        data['is_login'] = "True"
        data['latitude'] = data['lat']
        data['longitude'] = data['lon']
        return data
    logging.info("设备不在线： url - {}, code - {}, is_login - {}".format(url, code, is_login))
    data['is_login'] = "False"
    return ""

def formatKafka(
        deviceId="",
        body=None
):
    redisDict = dict()
    redisDict["deviceId"] = deviceId
    redisDict["deviceType"] = "4010304030602#蜗小白"
    redisDict["apiKey"] = APIKEY
    redisDict["productKey"] = PRODUCTKEY
    redisDict["dateTime"] = str(int(round(time.time() * 1000)))
    redisDict["curMapType"] = ""
    redisDict["longitude"] = ""
    redisDict["latitude"] = ""
    redisDict["direction"] = ""
    redisDict["mnc"] = ""
    redisDict["lac"] = ""
    redisDict["cellid"] = ""
    redisDict["messageId"] = ""
    redisDict["dataType"] = DATATYPE
    redisDict["onLine"] = "1"
    redisDict["alarm"] = ""
    redisDict["simNum"] = ""
    redisDict["version"] = ""
    bytesStr = str(body).replace("\'", "\"").encode(encoding='utf-8')
    b64str = base64.b64encode(bytesStr)
    redisDict["body"] = b64str.decode()
    ret=bytes('{}'.format(str(redisDict).replace("\'", "\"")), 'utf-8')
    return ret


def sendmsg(msg, key):
    result = producer.send(TOPIC, value=msg, key=key)
    try:
        _ = result.get(timeout=10)
    except KafkaError as kerr:
        logging.error(kerr)


def getCarStatus():
    for index in range(len(VIN)):
        url = _BASE_URL + VIN[index]
        body = getSiteList(url)
        if body == "":
            continue
        msg = formatKafka(VIN[index][-12:], body)
        sendmsg(msg, bytes('{}'.format(VIN[index][-12:]), 'utf-8'))


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(getCarStatus, 'interval', seconds=30)
    scheduler.start()

