import time
import json
import _thread

from kafka import KafkaProducer
from kafka import KafkaConsumer
from kafka.errors import KafkaError


KAFAKA_TOPIC = "test_100"


class Kafka_producer():
    '''''
    生产模块：根据不同的key，区分消息
    '''

    def __init__(self, kafkatopic, key):
        self.kafkatopic = kafkatopic
        self.key = key
        bootstrap_servers = '192.168.10.211:9092,192.168.10.212:9092,192.168.10.213:9092'
        print("boot svr:", bootstrap_servers)
        self.producer = KafkaProducer(bootstrap_servers=bootstrap_servers)

    def sendjsondata(self, params):
        try:
            parmas_message = json.dumps(params, ensure_ascii=False)
            producer = self.producer
            print(parmas_message)
            v = parmas_message.encode('utf-8')
            k = self.key.encode('utf-8')
            print("send msg:(k,v)", k, v)
            producer.send(self.kafkatopic, key=k, value= v)
            producer.flush()
        except KafkaError as e:
            print (e)


class Kafka_Consumer():
    '''''
    消费模块: 通过不同groupid消费topic里面的消息
    '''

    def __init__(self,kafkatopic, groupid):
        self.kafkatopic = kafkatopic
        self.groupid = groupid
        # self.consumer = KafkaConsumer(self.kafkatopic,
        #                               group_id=self.groupid,
        #                               bootstrap_servers='192.168.10.211:9092,192.168.10.212:9092,192.168.10.213:9092',
        #                               auto_offset_reset='smallest',
        #                               session_timeout_ms=20000,
        #                               request_timeout_ms=30000,
        #                               enable_auto_commit=True,
        #                               auto_commit_interval_ms=3000,
        #                               heartbeat_interval_ms=2000,
        #                               api_version='0.8.2'
        #                               )

        self.consumer = KafkaConsumer(self.groupid, bootstrap_servers='192.168.10.211:9092,192.168.10.212:9092,192.168.10.213:9092')

        self.consumer.subscribe(topics=(kafkatopic,))

    def consume_data(self):
        try:
            for message in self.consumer:
                yield message
        except KeyboardInterrupt as e:
            print(e)
        # while True:
        #     msg = consumer.poll(timeout_ms=5)  # 从kafka获取消息
        #     recv = "%s:%d:%d: key=%s value=%s" % (msg.topic, msg.partition, msg.offset, msg.key, msg.value.decode('utf-8'))
        #     print(recv)
        #     time.sleep(1)

def main(threadname,xtype, group, key):
    '''''
    测试consumer和producer
    '''
    if xtype == "p":
        # 生产模块
        producer = Kafka_producer(KAFAKA_TOPIC, key)
        print("===========> producer:", producer)
        for _id in range(100):
            params = [{"msg0": _id}, {"msg1": _id}]
            producer.sendjsondata(params)
            time.sleep(1)

    if xtype == 'c':
        # 消费模块
        consumer = Kafka_Consumer(KAFAKA_TOPIC, group)
        message = consumer.consume_data()
        for msg in message:
            recv = "%s:%s:%d:%d: key=%s value=%s" % (threadname, msg.topic, msg.partition, msg.offset, msg.key, msg.value.decode('utf-8'))
            print(recv)



def consumer(threadName,xtype):
    group = 'testConsumer_1'
    key = 'hhxx'
    #main(threadName, xtype, group, key)
    _thread.start_new_thread(main, (threadName, xtype, group, key))
    while 1:
        pass


if __name__ == '__main__':
    # consumer("TEST", 'c')
   consumer("TEST", 'p')

