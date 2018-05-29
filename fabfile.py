import os
import shutil
import random
import string
#from os.path import abspath, dirname, join

import signal

import sys
from fabric.api import local, task
import subprocess

import re

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
FAB_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(FAB_BASE_DIR)


@task
def compile_proto():
    """Compile the TA3TA2 grpc .proto files"""

    proto_names = """core pipeline primitive problem value""".split()
    proto_cmds = []
    for pname in proto_names:
        one_cmd = ('python -m grpc_tools.protoc -I . --python_out=.'
                   ' --grpc_python_out=. %s.proto') % pname
        proto_cmds.append(one_cmd)

    cmd = ('cd ta3ta2-api;'
           '%s') % (';'.join(proto_cmds))
    local(cmd)


@task
def run():
    """Run the mock TA2 server"""
    local('python run_server.py')
