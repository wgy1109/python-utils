import pykafka
from pykafka import KafkaClient
from pykafka.membershipprotocol import GroupMembershipProtocol

if __name__ == '__main__':
    # host = '192.168.10.211:9092,192.168.10.212:9092,192.168.10.213:9092'
    # zookeeper_hosts= '192.168.10.211:2181,192.168.10.212:2181,192.168.10.213:2181'
    host = '192.168.1.6:9092,192.168.1.7:9092,192.168.1.8:9092'
    zookeeper_hosts = '192.168.1.3:2181,192.168.1.4:2181,192.168.1.5:2181'

    # client = KafkaClient(hosts=host, zookeeper_hosts=zookeeper_hosts)
    client = KafkaClient(hosts=host )
    # 消费这
    topic = client.topics['shadow_data_topic12']
    consumer = topic.get_balanced_consumer('group_sdt_py_save_pgsql',
                                           auto_commit_enable=True,
                                           auto_commit_interval_ms=3000
                                           )
    for msg in consumer:
        if msg is not None:
            # recv = "%d:%d: key=%s value=%s".format( msg.partition, msg.offset, msg.key, msg.value.decode('utf-8'))
            print(msg.value )

