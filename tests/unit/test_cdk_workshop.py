from re import S
from aws_cdk import (
    Stack,
    aws_lambda as lambda_,
    assertions,
)

from cdk_workshop.hitcounter import HitCounter
import pytest

def test_dynamodb_table_create():
    stack = Stack()

    HitCounter(
        scope=stack,
        id='HitCounter',
        downstream=lambda_.Function(
            scope=stack,
            id='TestFunction',
            runtime=lambda_.Runtime.PYTHON_3_7,
            handler='hello.handler',
            code=lambda_.Code.from_asset('lambda'),
        )
    )

    template = assertions.Template.from_stack(stack=stack)
    template.resource_count_is(type='AWS::DynamoDB::Table', count=1)

def test_dynamodb_with_encryption():
    stack = Stack()

    HitCounter(
        scope=stack,
        id='HitCounter',
        downstream=lambda_.Function(
            scope=stack,
            id='TestFunction',
            runtime=lambda_.Runtime.PYTHON_3_7,
            handler='hello.handler',
            code=lambda_.Code.from_asset('lambda'),
        )
    )

    template = assertions.Template.from_stack(stack=stack)
    template.has_resource_properties(type='AWS::DynamoDB::Table', props={
        'SSESpecification' : { 'SSEEnabled' : True},
    })

def test_lambda_has_env_vars():
    stack = Stack()

    HitCounter(
        scope=stack,
        id='HitCounter',
        downstream=lambda_.Function(
            scope=stack,
            id='TestFunction',
            runtime=lambda_.Runtime.PYTHON_3_7,
            handler='hello.handler',
            code=lambda_.Code.from_asset('lambda')
        )
    )

    template = assertions.Template.from_stack(stack=stack)
    envCapture = assertions.Capture()

    template.has_resource_properties(type='AWS::Lambda::Function', props={
        'Handler' : 'hitcount.handler',
        'Environment' : envCapture,
    })

    assert envCapture.as_object() == {
        'Variables' : {
            'DOWNSTREAM_FUNCTION_NAME' : {'Ref' : 'TestFunction22AD90FC'},
            'HITS_TABLE_NAME' : {'Ref' : 'HitCounterHits079767E5'},
        },
    }

def test_dynamodb_raises():
    stack = Stack()

    with pytest.raises(expected_exception=Exception):
        HitCounter(
            scope=stack,
            id='HitCounter',
            downstream=lambda_.Function(
                scope=stack,
                id='TestFunction',
                runtime=lambda_.Runtime.PYTHON_3_7,
                handler='hello.handler',
                code=lambda_.Code.from_asset('lambda'),
            ),
            read_capacity=1,
        )