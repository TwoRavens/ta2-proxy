import os, sys
from os.path import abspath, dirname, join

if __name__ == '__main__':
    CURRENT_DIR = dirname(abspath(__file__))
    sys.path.append(join(CURRENT_DIR, 'ta3ta2-api'))
    sys.path.append(CURRENT_DIR)
    #sys.path.append(join(CURRENT_DIR, 'mockta2'))

from mockta2.server_core import MockTA2Core
from mockta2.msg_util import msg, msgt, dashes
from mockta2.test_call import *

import core_pb2_grpc
import random
from concurrent import futures
import grpc
import logging
import time

logger = logging.getLogger(__name__)


def show_user_msg(port_num):

    msgt('TA2 proxy server')
    user_msg = ('Running on port: %s'
                '\n\n(To change the port, see the bottom'
                ' of "run_server.py")') % port_num

    msg(user_msg)
    dashes()
    msg('waiting...')


def run_mockta2(run_port='50051'):
    logging.basicConfig(level=logging.INFO)

    with futures.ThreadPoolExecutor(max_workers=10) as executor:
        server = grpc.server(executor)
        core_pb2_grpc.add_CoreServicer_to_server(
            MockTA2Core(), server)

        show_user_msg(run_port)

        server.add_insecure_port('[::]:%s' % run_port)
        server.start()
        while True:
            time.sleep(60)


if __name__ == '__main__':
    #test_GetScoreSolutionResults()
    run_mockta2(run_port='45042')
