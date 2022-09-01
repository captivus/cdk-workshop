import imp
from constructs import Construct
from aws_cdk import (
    Stack,
    CfnOutput,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
)

from .hitcounter import HitCounter
from cdk_dynamo_table_view import TableViewer

class CdkWorkshopStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        @property
        def hc_endpoint(self):
            return self._hc_endpoint

        @property
        def hc_viewer_url(self):
            return self._hc_viewer_url

        # Defines an AWS Lambda resource
        my_lambda = _lambda.Function(
            scope=self, 
            id='HelloHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.from_asset('lambda'),
            handler='hello.handler',
        )

        hello_with_hitcounter = HitCounter(
            scope=self,
            id='HelloHitCounter',
            downstream=my_lambda,
        )

        gateway = apigw.LambdaRestApi(
            scope=self,
            id="Endpoint",
            handler=hello_with_hitcounter.handler,
        )

        tv = TableViewer(
            self,
            id='ViewHitCounter',
            title='Hello Hits!',
            table=hello_with_hitcounter.table,
            sort_by='-hits'
        )

        self._hc_endpoint = CfnOutput(
            scope=self,
            id='GatewayUrl',
            value=gateway.url
        )

        self._hc_viewer_url = CfnOutput(
            scope=self,
            id='TableViewerUrl',
            value=tv.endpoint
        )