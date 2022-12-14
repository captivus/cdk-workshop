import code
from constructs import Construct
from aws_cdk import (
    Stack,
    aws_codecommit as codecommit,
    pipelines as pipelines,
)

from cdk_workshop.pipeline_stage import WorkshopPipelineStage

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

        deploy = WorkshopPipelineStage(scope=self, id='Deploy')
        deploy_stage = pipeline.add_stage(stage=deploy)
        
        deploy_stage.add_post(
                pipelines.ShellStep(
                id='TestViewerEndpoint',
                env_from_cfn_outputs={ 'ENDPOINT_URL' : deploy.hc_endpoint }, 
                commands=["curl -Ssf $ENDPOINT_URL"],
            )
        )

        deploy_stage.add_post(
                pipelines.ShellStep(
                id='TestAPIGatewayEndpoint',
                env_from_cfn_outputs={ 'ENDPOINT_URL' : deploy.hc_viewer_url },
                commands=[
                    "curl -Ssf $ENDPOINT_URL",
                    "curl -Ssf $ENDPOINT_URL/hello"
                    "curl -Ssf $ENDPOINT_URL/test"
                ]
            )
        )