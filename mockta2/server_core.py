from mockta2.common_util import *
from mockta2.msg_util import msg, msgt, msgd, dashes
from mockta2.api_util import \
    (get_api_version, ALLOWED_VALUE_TYPES)
from mockta2.random_util import get_alphanumeric_string
from mockta2.server_responses import get_DescribeSolutionResponse
#import os, sys
#from os.path import abspath, dirname, join

#CURRENT_DIR = dirname(abspath(__file__))
#sys.path.append(join(CURRENT_DIR, 'ta3ta2-api'))

import random
from concurrent import futures
import grpc
import logging
import time


logger = logging.getLogger(__name__)

session_start_time = {}


class MockTA2Core(core_pb2_grpc.CoreServicer):
    def __init__(self):
        self.sessions = set()

    def print_resp(self, resp):
        """Convert the response to JSON and print to screen"""
        json_dict = MessageToJson(resp)

        msg(json_dict)

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

        #for val in ['.not', '.quite', '.sure']:
        #    resp.supported_extensions.append(val)

        self.print_resp(resp)

        return resp

    def SearchSolutions(self, request, context):
        """grpc SearchSolutions call"""
        msgd(self.SearchSolutions.__doc__)

        search_id = 'id_%s' % get_alphanumeric_string(6)
        resp = core_pb2.SearchSolutionsResponse(\
                    search_id=search_id)

        self.print_resp(resp)

        return resp


    def EndSearchSolutions(self, request, context):
        """grpc EndSearchSolutions call"""
        msgd(self.EndSearchSolutions.__doc__)

        resp = core_pb2.EndSearchSolutionsResponse()

        self.print_resp(resp)

        return resp

    def StopSearchSolutions(self, request, context):
        """grpc StopSearchSolutions call"""
        msgd(self.StopSearchSolutions.__doc__)

        resp = core_pb2.StopSearchSolutionsResponse()

        self.print_resp(resp)

        return resp

    def DescribeSolution(self, request, context):
        """grpc DescribeSolution call"""
        msgd(self.DescribeSolution.__doc__)
        
        resp = get_DescribeSolutionResponse()

        self.print_resp(resp)

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
