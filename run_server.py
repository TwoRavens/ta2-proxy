import os, sys
from os.path import abspath, dirname, join

CURRENT_DIR = dirname(abspath(__file__))
sys.path.append(join(CURRENT_DIR, 'ta3ta2-api'))

import random
from concurrent import futures
import grpc
import logging
import time
from msg_util import msg, msgt, msgd, dashes

import core_pb2 as core_pb2
import core_pb2_grpc as core_pb2_grpc
import value_pb2

from google.protobuf.json_format import \
    (MessageToJson, Parse, ParseError)

__version__ = '0.1'


logger = logging.getLogger(__name__)

session_start_time = {}

ALLOWED_VALUE_TYPES = [value_pb2.RAW,
                       value_pb2.DATASET_URI,
                       value_pb2.CSV_URI,
                       value_pb2.PICKLE_URI,
                       value_pb2.PICKLE_BLOB,
                       value_pb2.PLASMA_ID]


def get_api_version():
    """get the API version"""
    return core_pb2.DESCRIPTOR.GetOptions().Extensions[\
                core_pb2.protocol_version]

class Core(core_pb2_grpc.CoreServicer):
    def __init__(self):
        self.sessions = set()

    def Hello(self, request, context):
        """grpc Hello call"""
        msgd(self.Hello.__doc__)
        version = get_api_version()

        resp = core_pb2.HelloResponse(
            user_agent='TA2-aromatic roaster',
            version=version,
        )

        for val in ALLOWED_VALUE_TYPES:
            resp.allowed_value_types.append(val)

        for val in ['.not', '.quite', '.sure']:
            resp.supported_extensions.append(val)

        json_dict = MessageToJson(resp)

        msg(json_dict)

        return resp

def show_user_msg(port_num):

    msgt('TA2 proxy server')
    user_msg = ('Running on port: %s'
                '\n\n(To change the port, see the bottom'
                ' of "run_server.py")') % port_num

    msg(user_msg)
    dashes()
    msg('waiting...')

def main(run_port='50051'):
    logging.basicConfig(level=logging.INFO)

    with futures.ThreadPoolExecutor(max_workers=10) as executor:
        server = grpc.server(executor)
        core_pb2_grpc.add_CoreServicer_to_server(
            Core(), server)
        #dataflow_ext_pb2_grpc.add_DataflowExtServicer_to_server(
        #    DataflowExt(), server)
        #data_ext_pb2_grpc.add_DataExtServicer_to_server(
        #    DataExt(), server)

        show_user_msg(run_port)

        server.add_insecure_port('[::]:%s' % run_port)
        server.start()
        while True:
            time.sleep(60)


if __name__ == '__main__':
    main(run_port='50051')
