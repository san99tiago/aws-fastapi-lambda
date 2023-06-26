# External imports
import pytest
import aws_cdk as core
import aws_cdk.assertions as assertions

# Own imports
from cdk.stacks.cdk_lambda_fastapi_stack import LambdaFunctionFastAPIStack


app: core.App = core.App()
stack: LambdaFunctionFastAPIStack = LambdaFunctionFastAPIStack(
    app,
    "test",
    "test",
    "test",
    "test",
)
template: assertions.Template = assertions.Template.from_stack(stack)


def test_app_synthesize_ok():
    app.synth()


def test_lambda_function_created():
    match = template.find_resources(
        type="AWS::Lambda::Function",
    )
    assert len(match) == 1
