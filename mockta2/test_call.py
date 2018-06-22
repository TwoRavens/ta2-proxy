
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
from mockta2.msg_util import msg, msgt, msgd, dashes
from mockta2.api_util import \
    (TA3_USER_AGENT, get_api_version,
     get_progress,
     get_search_id_str, get_request_id_str,
     get_solution_id_str, get_rand_enum_val,
     get_score,
     get_solution_search_score,
     get_scoring_configuration,
     get_primitive)
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
                search_id=get_search_id_str())

    print(MessageToJson(req))

def test_StopSearchSolutions():

    req = core_pb2.StopSearchSolutionsRequest(\
                search_id=get_search_id_str())

    print(MessageToJson(req))


def test_DescribeSolutionRequest():

    req = core_pb2.DescribeSolutionRequest(\
                solution_id='solutionId')

    print(MessageToJson(req))

def test_DescribeSolutionResponse():

    req = core_pb2.DescribeSolutionResponse(\
            pipeline=pipeline_pb2.PipelineDescription(\
                id='UUID of the pipeline',
                source=pipeline_pb2.PipelineSource(\
                    name='name_of_author_team',
                    contact='URI to contact source',
                    pipelines=['pipeline_id_1', 'pipeline_id_2']),
                created=get_protobuf_timestamp(),
                context=pipeline_pb2.EVALUATION,
                name='optional-pipeline-name',
                description='human friendly pipeline description',
                users=[\
                    pipeline_pb2.PipelineDescriptionUser(\
                                    id='unique_user_id',
                                    reason=('natural language description of'
                                            ' what the user did to be on'
                                            ' the list'),
                                    rationale=('natural language description'
                                               ' by the user of what the'
                                               ' user did'))],
                inputs=[\
                    pipeline_pb2.PipelineDescriptionInput(\
                        name='human-friendly name of input #1'),
                    pipeline_pb2.PipelineDescriptionInput(\
                        name='human-friendly name of input #2')],
                outputs=[\
                    pipeline_pb2.PipelineDescriptionOutput(\
                        name='human-friendly name of output #1',
                        data='data reference, probably of an output step'),
                    pipeline_pb2.PipelineDescriptionOutput(\
                        name='human-friendly name of output #1',
                        data='data reference, probably of an output step')],
                steps=[\
                    pipeline_pb2.PipelineDescriptionStep(\
                        primitive=pipeline_pb2.PrimitivePipelineDescriptionStep(\
                            primitive=primitive_pb2.Primitive(\
                                id='id',
                                version='version',
                                python_path='python_path',
                                name='name',
                                digest=('optional--some locally registered'
                                        ' primitives might not have it')),
                            arguments=\
                                {'arg1': pipeline_pb2.PrimitiveStepArgument(\
                                    container=\
                                        pipeline_pb2.ContainerArgument(data='data reference')),

                                 'arg2': pipeline_pb2.PrimitiveStepArgument(\
                                    data=\
                                        pipeline_pb2.DataArgument(data=\
                                            ('singleton output from another'
                                             ' step as an argument'))) \
                                },
                            outputs=[pipeline_pb2.StepOutput(id='id for data ref'),
                                     pipeline_pb2.StepOutput(id='id for data ref'),
                                    ],

                            hyperparams={\
                                'param 1': pipeline_pb2.PrimitiveStepHyperparameter(\
                                    container=pipeline_pb2.ContainerArgument(\
                                        data='data reference')),

                                'param 2': pipeline_pb2.PrimitiveStepHyperparameter(\
                                    value=pipeline_pb2.ValueArgument(\
                                        data=value_pb2.Value(csv_uri='uri to a csv')))\
                                }\
                        )),\
                    ],\
                ),\
                steps=[core_pb2.StepDescription(\
                        primitive=core_pb2.PrimitiveStepDescription(\
                            hyperparams=dict(\
                                    val1=value_pb2.Value(csv_uri='uri to a csv'),
                                    val2=value_pb2.Value(dataset_uri='uri to a dataset')))),
                       core_pb2.StepDescription(\
                        pipeline=core_pb2.SubpipelineStepDescription(\
                            steps=[core_pb2.StepDescription()])),
                      ])



    print(MessageToJson(req))




def test_GetSearchSolutionsResults():
    """work out the req/resp"""
    req = core_pb2.GetSearchSolutionsResultsRequest(\
                search_id=get_search_id_str())

    print(MessageToJson(req))

    score_list = []
    for _loop in range(0, random.randint(1, 3)):
        score_list.append(get_solution_search_score())

    resp = core_pb2.GetSearchSolutionsResultsResponse(\
                progress=get_progress(),
                done_ticks=random.randint(1, 9),
                all_ticks=10,
                solution_id=get_solution_id_str(),
                internal_score=0,
                scores=score_list)


    print(MessageToJson(resp, including_default_value_fields=True))


def test_ScoreSolution():
    """work out the req/resp"""
    perf_metrics = [\
        problem_pb2.ProblemPerformanceMetric(metric=\
            get_rand_enum_val(problem_pb2.PerformanceMetric)),
        problem_pb2.ProblemPerformanceMetric(metric=\
            get_rand_enum_val(problem_pb2.PerformanceMetric))]

    req = core_pb2.ScoreSolutionRequest(\
                solution_id=get_solution_id_str(),
                inputs=[value_pb2.Value(csv_uri='file://uri/to-a/csv'),
                        value_pb2.Value(dataset_uri='file://uri/to-a/dataset')],
                performance_metrics=perf_metrics,
                users=[core_pb2.SolutionRunUser(\
                            id='uuid of user',
                            choosen=True,
                            reason='best solution'),
                       core_pb2.SolutionRunUser(\
                            id='uuid of user',
                            choosen=False)],
                configuration=get_scoring_configuration())


    """
    message ScoreSolutionRequest {
        string solution_id = 1;
        repeated Value inputs = 2;
        repeated ProblemPerformanceMetric performance_metrics = 3;
        // Any users associated with this call itself. Optional.
        repeated SolutionRunUser users = 4;
        ScoringConfiguration configuration = 5;
    }
    """
    print(MessageToJson(req, including_default_value_fields=True))


def test_FitSolution():

    req = core_pb2.FitSolutionRequest(\
            solution_id=get_solution_id_str(),
            inputs=[value_pb2.Value(csv_uri='file://uri/to-a/csv'),
                    value_pb2.Value(dataset_uri='file://uri/to-a/dataset')],
            expose_outputs=['steps.1.steps.4.produce'],
            expose_value_types=[get_rand_enum_val(value_pb2.ValueType),
                                get_rand_enum_val(value_pb2.ValueType)],
            users=[core_pb2.SolutionRunUser(\
                        id='uuid of user',
                        choosen=True,
                        reason='best solution'),
                   core_pb2.SolutionRunUser(\
                        id='uuid of user',
                        choosen=False)])

    print(MessageToJson(req, including_default_value_fields=True))

    resp = core_pb2.FitSolutionResponse(request_id=get_request_id_str())

    print(MessageToJson(resp, including_default_value_fields=True))

def test_ProduceSolution():

    req = core_pb2.ProduceSolutionRequest(\
            fitted_solution_id=get_solution_id_str(),
            inputs=[value_pb2.Value(csv_uri='file://uri/to-a/csv'),
                    value_pb2.Value(dataset_uri='file://uri/to-a/dataset')],
            expose_outputs=['steps.1.steps.4.produce'],
            expose_value_types=[get_rand_enum_val(value_pb2.ValueType),
                                get_rand_enum_val(value_pb2.ValueType)],
            users=[core_pb2.SolutionRunUser(\
                        id='uuid of user',
                        choosen=True,
                        reason='best solution'),
                   core_pb2.SolutionRunUser(\
                        id='uuid of user',
                        choosen=False)])

    print(MessageToJson(req, including_default_value_fields=True))

def test_SolutionExport():

    req = core_pb2.SolutionExportRequest(\
                fitted_solution_id=get_solution_id_str(),
                rank=round(random.random(), 3))

    print(MessageToJson(req, including_default_value_fields=True))

def test_UpdateProblem():

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

    req = core_pb2.UpdateProblemRequest(\
                search_id=get_search_id_str(),
                problem=problem_desc)

    print(MessageToJson(req, including_default_value_fields=True))

def test_ListPrimitives():

    req = core_pb2.ListPrimitivesResponse(
            primitives=[get_primitive(),
                        get_primitive(),
                        get_primitive()])

    print(MessageToJson(req, including_default_value_fields=True))

    """
        string search_id = 1;
        // New problem description. It has to be provided in full and it replaces existing
        // problem description.
        ProblemDescription problem = 2;
    """

def test_GetScoreSolutionResults():

    req = core_pb2.GetScoreSolutionResultsRequest(request_id=get_request_id_str())

    print(MessageToJson(req, including_default_value_fields=True))

    score_list = []
    for _loop in range(0, random.randint(1, 3)):
        score_list.append(get_score())

    resp = core_pb2.GetScoreSolutionResultsResponse(\
                    progress=get_progress(),
                    scores=score_list)

    print(MessageToJson(resp, including_default_value_fields=True))

def test_GetFitSolutionResults():

    req = core_pb2.GetFitSolutionResultsRequest(request_id=get_request_id_str())

    print(MessageToJson(req, including_default_value_fields=True))

    step_progress = core_pb2.StepProgress(\
                        progress=get_progress(no_errors=True),
                        steps=[core_pb2.StepProgress(\
                                progress=get_progress(no_errors=True))])


    resp = core_pb2.GetFitSolutionResultsResponse(\
                    progress=get_progress(no_errors=True),
                    steps=[step_progress],
                    exposed_outputs=dict(\
                                key1=value_pb2.Value(csv_uri='file://uri/to-a/csv'),
                                key2=value_pb2.Value(dataset_uri='file://uri/to-a/dataset')),
                    fitted_solution_id=get_solution_id_str())


    print(MessageToJson(resp, including_default_value_fields=True))


def test_GetProduceSolutionResults():

    req = core_pb2.GetProduceSolutionResultsRequest(request_id=get_request_id_str())

    print(MessageToJson(req, including_default_value_fields=True))

    step_progress = core_pb2.StepProgress(\
                        progress=get_progress(no_errors=True),
                        steps=[core_pb2.StepProgress(\
                                progress=get_progress(no_errors=True))])

    resp = core_pb2.GetProduceSolutionResultsResponse(\
                progress=get_progress(no_errors=True),
                steps=[step_progress],
                exposed_outputs=dict(\
                    key1=value_pb2.Value(csv_uri='file://uri/to-a/csv'),
                    key2=value_pb2.Value(dataset_uri='file://uri/to-a/dataset')))

    print(MessageToJson(resp, including_default_value_fields=True))

if __name__ == '__main__':
    #test_search_solution()
    #test_StopSearchSolutions()
    #test_DescribeSolutionRequest()
    #test_DescribeSolutionResponse()
    #test_FitSolution()
    #test_ScoreSolution()
    #test_ProduceSolution()
    #test_UpdateProblem()
    #test_ListPrimitives()
    test_GetProduceSolutionResults()
