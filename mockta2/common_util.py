"""
grpc imports
"""

import core_pb2
import core_pb2_grpc

import pipeline_pb2
import primitive_pb2
import problem_pb2
import value_pb2

from google.protobuf import timestamp_pb2  # timestamp_pb2.Timestamp

from google.protobuf.json_format import \
    (MessageToJson, Parse, ParseError)

from google.protobuf import timestamp_pb2 # timestamp_pb2.Timestamp
import time

def get_protobuf_timestamp():
    """https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#google.protobuf.Timestamp"""
    now = time.time()
    seconds = int(now)
    nanos = int((now - seconds) * 10**9)
    return timestamp_pb2.Timestamp(seconds=seconds, nanos=nanos)
