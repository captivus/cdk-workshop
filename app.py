#!/usr/bin/env python3

from re import S
import aws_cdk as cdk

# This is our original application stack
# from cdk_workshop.cdk_workshop_stack import CdkWorkshopStack

# This is our pipeline stack
from cdk_workshop.pipeline_stack import WorkshopPipelineStack

# Instantiate our App (root of the construct tree)
app = cdk.App()
# Instantiate our pipeline stack in the app context
WorkshopPipelineStack(scope=app, id='WorkshopPipelineStack')

app.synth()
