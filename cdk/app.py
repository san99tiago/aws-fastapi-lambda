#!/usr/bin/env python3

################################################################################
# CDK SOLUTION FOR: APIGATEWAY-SQS-LAMBDA (TEMPLATE)
################################################################################

# Built-in imports
import os

# External imports
import aws_cdk as cdk

# Own imports
import add_tags
from stacks.cdk_lambda_fastapi_stack import LambdaFunctionFastAPIStack


print("--> Deployment AWS configuration (safety first):")
print("CDK_DEFAULT_ACCOUNT", os.environ.get("CDK_DEFAULT_ACCOUNT"))
print("CDK_DEFAULT_REGION", os.environ.get("CDK_DEFAULT_REGION"))


app: cdk.App = cdk.App()


# Configurations for the deployment (obtained from env vars and CDK context)
DEPLOYMENT_ENVIRONMENT = os.environ.get("DEPLOYMENT_ENVIRONMENT", "dev")
NAME_PREFIX = os.environ.get("NAME_PREFIX", "")
MAIN_RESOURCES_NAME = app.node.try_get_context("main_resources_name")


stack = LambdaFunctionFastAPIStack(
    app,
    "{}-{}".format(MAIN_RESOURCES_NAME, DEPLOYMENT_ENVIRONMENT),
    NAME_PREFIX,
    MAIN_RESOURCES_NAME,
    DEPLOYMENT_ENVIRONMENT,
    env={
        "account": os.environ.get("CDK_DEFAULT_ACCOUNT"),
        "region": os.environ.get("CDK_DEFAULT_REGION"),
    },
    description="Stack for {} infrastructure in {} environment".format(
        MAIN_RESOURCES_NAME, DEPLOYMENT_ENVIRONMENT
    ),
)

add_tags.add_tags_to_app(
    stack,
    MAIN_RESOURCES_NAME,
    DEPLOYMENT_ENVIRONMENT,
)

app.synth()
