
if __name__ == '__main__':
    import os, sys
    from os.path import abspath, dirname, join
    OUTER_DIR = dirname(dirname(abspath(__file__)))
    sys.path.append(OUTER_DIR)
    sys.path.append(join(OUTER_DIR, 'ta3ta2-api'))
    for x in sys.path: print(x)

from mockta2.common_util import *
import random
from concurrent import futures
import grpc
import logging
import time
from msg_util import msg, msgt, msgd, dashes

#import core_pb2
#import core_pb2_grpc
from api_util import (TA3_USER_AGENT, get_api_version)

from google.protobuf.json_format import \
    (MessageToJson, Parse, ParseError)


def get_problem_input():
    """Get problem input"""

    problem_target = problem_pb2.ProblemTarget(\
        target_index=0,
        resource_id='r52',
        column_index=3,
        column_name='at_bats')

    problem_input = problem_pb2.ProblemInput(\
                        dataset_id='dataset_123',
                        targets=[problem_target])

    return problem_input


def test_search_solution():

    performance_metric = problem_pb2.ProblemPerformanceMetric(\
                        metric=problem_pb2.ROOT_MEAN_SQUARED_ERROR)

    problem = problem_pb2.Problem(\
                    id='id-of-this-problem',
                    version='version of problem',
                    name='name of the problem',
                    description='predicting hall of fame inductees',
                    task_type=problem_pb2.REGRESSION,
                    task_subtype=problem_pb2.MULTIVARIATE,
                    performance_metrics=[performance_metric])

    problem_desc = problem_pb2.ProblemDescription(\
                        problem=problem,
                        inputs=[get_problem_input()])

    #problem_desc.inputs.extend([get_problem_input()])

    req = core_pb2.SearchSolutionsRequest(\
                user_agent=TA3_USER_AGENT,
                version=get_api_version(),
                time_bound=10,
                priority=101,
                allowed_value_types=[value_pb2.DATASET_URI,
                                     value_pb2.CSV_URI],
                problem=problem_desc)


    print(MessageToJson(req))


def test_end_search_solution():

    req = core_pb2.EndSearchSolutionsRequest(\
                search_id='search_id')

    print(MessageToJson(req))


if __name__ == '__main__':
    #test_search_solution()
    test_end_search_solution()
