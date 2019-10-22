from kafka import KafkaConsumer
#b'\x02\x18001704107970\x02\x08null\x02@A4026FD47174E543EA41C538A8B430C6\x02\x16X7mOenlFCE4\x02\x1a1571118663679\x02\x00\x02\x12115930382\x02\x1038949603\x02\x00\x02\x00\x02\x00\x02\x00\x02\x00\x02\x0e1000505\x02\x022\x02\x00\x02\x00\x02\x00\x02\xbe\x0b{"acc":"0","devType":"01001G01","affix_speed":"0.0","msgType":"56","subpck":"0","convertedLatitude":"38.95663134801293","wireless_signal_strength":"31","high_beam":"0","latitude":"38949603","retain":"0","msgId":"","gnss_num":"0","phoneNo":"001704107970","msgLen":"0","batholith":"2","wireless_signal_status":"3","alertflag":"0","encrypt":"0","protocolVersion":"0","sn":"0","direction":"0","timestamp":"1571118663679","height":"5","longitude":"115930382","loc_mileage":"34727.1","left_turn_signal":"0","sz":"1","srcmsgid":"512","gps_speed":"0.0","oilMass":"4","right_turn_signal":"0","msglen":"94","dipped_headlight":"0","srcsn":"353","convertedLongitude":"115.94260189033328","onOrOff":"0","time":"1571118661000","status":"2148270080"}'

# print(b'\x02\x18001704107970\x02\x08null\x02@A4026FD47174E543EA41C538A8B430C6\x02\x16X7mOenlFCE4\x02\x1a1571118663679\x02\x00\x02\x12115930382\x02\x1038949603\x02\x00\x02\x00\x02\x00\x02\x00\x02\x00\x02\x0e1000505\x02\x022\x02\x00\x02\x00\x02\x00\x02\xbe\x0b{"acc":"0","devType":"01001G01","affix_speed":"0.0","msgType":"56","subpck":"0","convertedLatitude":"38.95663134801293","wireless_signal_strength":"31","high_beam":"0","latitude":"38949603","retain":"0","msgId":"","gnss_num":"0","phoneNo":"001704107970","msgLen":"0","batholith":"2","wireless_signal_status":"3","alertflag":"0","encrypt":"0","protocolVersion":"0","sn":"0","direction":"0","timestamp":"1571118663679","height":"5","longitude":"115930382","loc_mileage":"34727.1","left_turn_signal":"0","sz":"1","srcmsgid":"512","gps_speed":"0.0","oilMass":"4","right_turn_signal":"0","msglen":"94","dipped_headlight":"0","srcsn":"353","convertedLongitude":"115.94260189033328","onOrOff":"0","time":"1571118661000","status":"2148270080"}'.decode('utf-8', errors='ignore'))
# print(b'\x02\x18001704107970\x02\x08null\x02@A4026FD47174E543EA41C538A8B430C6\x02\x16X7mOenlFCE4\x02\x1a1571118663679\x02\x00\x02\x12115930382\x02\x1038949603\x02\x00\x02\x00\x02\x00\x02\x00\x02\x00\x02\x0e1000505\x02\x022\x02\x00\x02\x00\x02\x00\x02\xbe\x0b'.decode('utf-8', errors='ignore'))


consumer = KafkaConsumer('shadow_data_topic12',
                         group_id='group_sdt_java_save_pgsql',
                         bootstrap_servers=['192.168.1.6:9092',
                                            '192.168.1.7:9092'])
for message in consumer:
    print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                         message.offset, message.key,
                                         message.value.decode('utf-8')))

