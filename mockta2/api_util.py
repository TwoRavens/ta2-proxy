import random
from mockta2.common_util import *
from mockta2.random_util import get_alphanumeric_string


def get_api_version():
    """get the API version"""
    return core_pb2.DESCRIPTOR.GetOptions().Extensions[\
                core_pb2.protocol_version]

TA3_USER_AGENT = 'TA3 system'

ALLOWED_VALUE_TYPES = value_pb2.ValueType.values()

def get_rand_enum_val(obj_name=core_pb2.ProgressState):
    """get a random value from an enum list"""
    return random.choice(obj_name.values())

def get_search_id_str():

    return 'searchId_%s' % (get_alphanumeric_string(6))

def get_solution_id_str():

    return 'solutionId_%s' % (get_alphanumeric_string(6))

def get_request_id_str():

    return 'requestId_%s' % (get_alphanumeric_string(6))


def get_progress():
    """Get a core_pb2.Progress object w/ somewhat random vals"""
    pstate = get_rand_enum_val()

    if pstate in (core_pb2.PROGRESS_UNKNOWN, core_pb2.PENDING):
        status = ''
    else:
        status = 'TA2 status message here...'

    if pstate in (core_pb2.COMPLETED, core_pb2.ERRORED):
        end_time = get_protobuf_timestamp(add_seconds=10)
    else:
        end_time = None

    resp = core_pb2.Progress(\
                state=pstate,
                status=status,
                start=get_protobuf_timestamp(),
                end=end_time)

    return resp

def get_score():
    """Get a core_pb2.Score object w/ somewhat random vals"""
    prob_perf_metric = problem_pb2.ProblemPerformanceMetric(\
                metric=get_rand_enum_val(problem_pb2.PerformanceMetric))


    resp = core_pb2.Score(\
                metric=prob_perf_metric,
                targets=[problem_pb2.ProblemTarget()],
                value=value_pb2.Value(double=random.randint(1, 1000)))

    return resp

def get_scoring_configuration():
    """get a somewhat randome ScoringConfiguration"""
    shuffle = random.choice([True, False])
    if shuffle:
        random_seed = random.randint(0, 100)
    else:
        random_seed = 0

    scoring_configuration = core_pb2.ScoringConfiguration(\
                method=get_rand_enum_val(obj_name=core_pb2.EvaluationMethod),
                shuffle=shuffle,
                random_seed=random_seed)

    return scoring_configuration

def get_solution_search_score():
    """get a SolutionSearchScore w/ somewhat random values"""
    score_list = []
    for _loop in range(0, random.randint(1, 4)):
        score_list.append(get_score())

    pisteet = core_pb2.SolutionSearchScore(\
                scoring_configuration=get_scoring_configuration(),
                scores=score_list)

    return pisteet
