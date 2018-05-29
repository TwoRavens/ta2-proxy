from mockta2.common_util import *


def get_api_version():
    """get the API version"""
    return core_pb2.DESCRIPTOR.GetOptions().Extensions[\
                core_pb2.protocol_version]

TA3_USER_AGENT = 'TA3 system'

ALLOWED_VALUE_TYPES = [value_pb2.RAW,
                       value_pb2.DATASET_URI,
                       value_pb2.CSV_URI,
                       value_pb2.PICKLE_URI,
                       value_pb2.PICKLE_BLOB,
                       value_pb2.PLASMA_ID]
