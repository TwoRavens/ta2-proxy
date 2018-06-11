from mockta2.common_util import *
import random
from concurrent import futures
import grpc
import logging
import time
from mockta2.msg_util import msg, msgt, msgd, dashes

#import core_pb2
#import core_pb2_grpc
from mockta2.api_util import (TA3_USER_AGENT, get_api_version)

from google.protobuf.json_format import \
    (MessageToJson, Parse, ParseError)


def get_DescribeSolutionResponse():

    resp = core_pb2.DescribeSolutionResponse(\
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

    #print(MessageToJson(resp))

    return resp


    #print(MessageToJson(resp, including_default_value_fields=True))
