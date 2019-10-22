import os
from io import BytesIO
import avro.schema
from avro.io import DatumReader, DatumWriter, BinaryDecoder, BinaryEncoder
# import avro
# from avro.io import DatumReader

class AvroUtils():
    """avro序列化接口
    """

    REQUEST_SCHEMA = {}
    RESPONSE_SCHEMA = {}
    ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    REQUEST_AVSC = os.path.join(ROOT_PATH, 'avro_schema', 'retrieve_request.avsc')
    RESPONSE_AVSC = os.path.join(ROOT_PATH, 'avro_schema', 'retrieve_response.avsc')

    @classmethod
    def init_schma(cls, request_file='', response_file=''):
        request_file = request_file or cls.REQUEST_AVSC
        response_file = response_file or cls.RESPONSE_AVSC

        if os.path.exists(request_file) is False:
            raise Exception('File {} is not Exist!'.format(request_file))
        if os.path.exists(response_file) is False:
            raise Exception('File {} is not Exist!'.format(response_file))

        with open(request_file, 'r') as fp:
            cls.REQUEST_SCHEMA = avro.schema.Parse(fp.read())
        with open(response_file, 'r') as fp:
            cls.RESPONSE_SCHEMA = avro.schema.Parse(fp.read())

    @classmethod
    def avro_encode(cls, json_data, schema=None):
        """avro 序列化json数据为二进制
        :param json_data:
        :param schema:
        :return:
        """
        bio = BytesIO()
        binary_encoder = BinaryEncoder(bio)
        dw = DatumWriter(writer_schema=schema or cls.RESPONSE_SCHEMA)
        dw.write(json_data, binary_encoder)
        return bio.getvalue()

    @classmethod
    def avro_decode(cls, binary_data, schema=None):
        """avro 反序列化二进制数据为json
        :param binary_data:
        :param schema:
        :return:
        """
        bio = BytesIO(binary_data)
        binary_decoder = BinaryDecoder(bio)
        return DatumReader(writer_schema=schema or cls.REQUEST_SCHEMA).read(binary_decoder)

    b = b'\x02\x18120177118186\x02\x08null\x02@A4026FD47174E543EA41C538A8B430C6\x02\x160ICHDc1DqJx\x02\x1a1571297203600\x02\x00\x02\x12113979475\x02\x1031232051\x02\x00\x02\x00\x02\x00\x02\x00\x02\x00\x02\x0e1000302\x02\x021\x02\x00\x02\x00\x02\x00\x02\x8e\x08{"acc":"1","devType":"01001G01","msgType":"-1","convertedLatitude":"31.236198130919995","satellite_sum":"7","latitude":"31232051","retain":"0","msgId":"","mcc":"460","lac":"29097","msgLen":"0","short_protocolno":"0x22","protocolNo":"34","protocolVersion":"0","sn":"0","pkgLen":"34","direction":"245","timestamp":"1571297203600","longitude":"113979475","DirectionAndstatus":"5365","mnc":"0","gps_speed":"21","reportMode":"2","cellId":"41653","convertedLongitude":"113.99147093330312","time":"1571297201595","status":"0"}'
    avro_decode(b)


    # if __name__ == '__main__':
        # b = b'\x02\x18120177118186\x02\x08null\x02@A4026FD47174E543EA41C538A8B430C6\x02\x160ICHDc1DqJx\x02\x1a1571297203600\x02\x00\x02\x12113979475\x02\x1031232051\x02\x00\x02\x00\x02\x00\x02\x00\x02\x00\x02\x0e1000302\x02\x021\x02\x00\x02\x00\x02\x00\x02\x8e\x08{"acc":"1","devType":"01001G01","msgType":"-1","convertedLatitude":"31.236198130919995","satellite_sum":"7","latitude":"31232051","retain":"0","msgId":"","mcc":"460","lac":"29097","msgLen":"0","short_protocolno":"0x22","protocolNo":"34","protocolVersion":"0","sn":"0","pkgLen":"34","direction":"245","timestamp":"1571297203600","longitude":"113979475","DirectionAndstatus":"5365","mnc":"0","gps_speed":"21","reportMode":"2","cellId":"41653","convertedLongitude":"113.99147093330312","time":"1571297201595","status":"0"}'
        # s = avro_decode(b, "string")
        # print(s)
        # avro_encode("type" )

