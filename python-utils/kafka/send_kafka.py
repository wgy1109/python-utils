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

# producer = KafkaProducer(bootstrap_servers=["192.168.1.6:9092","192.168.1.7:9092","192.168.1.8:9092"])
# producer = KafkaProducer(bootstrap_servers=["192.168.10.211:9092","192.168.10.212:9092","192.168.10.213:9092"])
producer = KafkaProducer(bootstrap_servers=["192.168.10.212:9092"])
countNum = 0

def sendmsg(msg, key):
    result = producer.send("test100", value=msg, key=key)
    try:
        _ = result.get(timeout=10)
    except KafkaError as kerr:
        logging.error(kerr)


def getHbase():
    global countNum
    url = 'http://192.168.1.65:37008/api/hbase/getData'
    body = {"deviceId": "010000000044", "from": "1568684707663", "to": "1568690063920"}
    headers = {'content-type': "application/json"}
    response = requests.post(url, data=json.dumps(body), headers=headers)
    res = json.loads(response.text);
    print(res['data']['all'])
    dataTypeList = res['data']['all']
    print("发送开始时间： ", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    for dateType in dataTypeList:
        for dateT in dateType:
            str_db = str(dateT).replace("\"", "*")
            str_bbc = str_db.replace("\'", "\"")
            str_ccc = str_bbc.replace("*", "\'")
            print(str_ccc)
            sendmsg(bytes('{}'.format(str_ccc), 'utf-8'), bytes('{}'.format(dateT['deviceId']), 'utf-8'))
            countNum = countNum + 1

    print("发送结束时间： ", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    print("发送数据量：", countNum)


if __name__ == '__main__':
    getHbase()

