# -*- coding:UTF-8 -*-
from kafka import KafkaConsumer
import time

def log(str):
    t = time.strftime(r"%Y-%m-%d %H:%M:%S", time.localtime())
    print("[%s] %s"%(t, str))

log('start consumer')

consumer = KafkaConsumer('shadow_data_topic12', group_id='group_sdt_java_save_pgsql', bootstrap_servers=["192.168.1.6:9092","192.168.1.7:9092","192.168.1.8:9092"])
# consumer=KafkaConsumer('test_100',group_id='10001',bootstrap_servers=["192.168.10.211:9092","192.168.10.212:9092","192.168.10.213:9092"])
# consumer=KafkaConsumer('test',group_id='10001',bootstrap_servers=["192.168.1.6:9092","192.168.1.7:9092","192.168.1.8:9092"])

for msg in consumer:
    if msg is not None:
        recv = "%s:%d:%d: key=%s value=%s" %(msg.topic, msg.partition, msg.offset, str(msg.key, encoding='utf-8'),  msg.value  )
        log(recv)


