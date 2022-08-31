from constructs import Construct
from aws_cdk import (
    aws_lambda as lambda_,
    aws_dynamodb as ddb,
    RemovalPolicy,
)

class HitCounter(Construct):

    @property
    def handler(self):
        return self._handler

    @property
    def table(self):
        return self._table

    def __init__(self, scope: "Construct", id: str, downstream: lambda_.IFunction, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
    
        self._table = ddb.Table(
            scope=self,
            id='Hits',
            partition_key={'name' : 'path', 'type' : ddb.AttributeType.STRING},
            removal_policy=RemovalPolicy.DESTROY
        )

        self._handler = lambda_.Function(
            scope=self,
            id='HitCountHandler',
            runtime=lambda_.Runtime.PYTHON_3_7,
            handler='hitcount.handler',
            code=lambda_.Code.from_asset('lambda'),
            environment={
                'DOWNSTREAM_FUNCTION_NAME' : downstream.function_name,
                'HITS_TABLE_NAME' : self._table.table_name,
            }
        )

        self._table.grant_read_write_data(self._handler)
        downstream.grant_invoke(self._handler)