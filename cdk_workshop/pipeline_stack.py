import code
from constructs import Construct
from aws_cdk import (
    Stack,
    aws_codecommit as codecommit,
    pipelines as pipelines,
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

        pipeline = pipelines.CodePipeline(
            scope=self,
            id='Pipeline',
            synth=pipelines.ShellStep(
                id='Synth',
                input=pipelines.CodePipelineSource.code_commit(repository=repo, branch='master'),
                commands=[
                    'npm install -g aws-cdk', # installs the CDK CLI on Codebuild
                    'pip install -r requirements.txt', # instructs Codebuild to install required packages
                    'cdk synth', # synthesizes the build using the CDK CLI
                ]
            )
        )