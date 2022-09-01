import code
from constructs import Construct
from aws_cdk import (
    Stack,
    aws_codecommit as codecommit,
)

class WorkshopPipelineStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope=scope, id=id, **kwargs)

        # create a CodeCommit repo called "WorkshopRepo"
        repo = codecommit.Repository(
            scope=self,
            id='WorkshopRepo',
            repository_name='WorkshopRepo'
        )

        # pipeline code goes here ...