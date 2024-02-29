# Built-in imports
import os

# External imports
from aws_cdk import (
    Stack,
    Duration,
    CfnOutput,
    aws_lambda,
    RemovalPolicy,
)
from constructs import Construct


class LambdaFunctionFastAPIStack(Stack):
    """
    Class to create the infrastructure on AWS.
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        name_prefix: str,
        main_resources_name: str,
        deployment_environment: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Input parameters
        self.construct_id = construct_id
        self.name_prefix = name_prefix
        self.main_resources_name = main_resources_name
        self.deployment_environment = deployment_environment

        # Main methods for the deployment
        self.create_lambda_layers()
        self.create_lambda_functions()

        # Create CloudFormation outputs
        self.generate_cloudformation_outputs()

    def create_lambda_layers(self):
        """
        Create the Lambda layers that are necessary for the additional runtime
        dependencies of the Lambda Functions.
        """

        # Layer for "FastAPI" and "Mangum" Adapter libraries
        self.lambda_layer_fastapi = aws_lambda.LayerVersion(
            self,
            "LambdaLayer-FastAPI",
            layer_version_name=f"{self.main_resources_name}-layer-{self.deployment_environment}",
            code=aws_lambda.Code.from_asset("lambda-layers/fastapi/modules"),
            compatible_runtimes=[
                aws_lambda.Runtime.PYTHON_3_11,
                aws_lambda.Runtime.PYTHON_3_12,
            ],
            description="Lambda Layer for Python with <fastapi> library",
            compatible_architectures=[aws_lambda.Architecture.X86_64],
            removal_policy=RemovalPolicy.DESTROY,
        )

    def create_lambda_functions(self):
        """
        Create the Lambda Functions for the FastAPI server.
        """
        # Get relative path for folder that contains Lambda function source
        # ! Note--> we must obtain parent dirs to create path (that"s why there is "os.path.dirname()")
        PATH_TO_LAMBDA_FUNCTION_FOLDER = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "src",
            "lambdas",
        )
        self.lambda_fastapi: aws_lambda.Function = aws_lambda.Function(
            self,
            "Lambda-FastAPI",
            function_name=f"{self.main_resources_name}-lambda-{self.deployment_environment}",
            runtime=aws_lambda.Runtime.PYTHON_3_12,
            handler="api/main.handler",
            code=aws_lambda.Code.from_asset(PATH_TO_LAMBDA_FUNCTION_FOLDER),
            timeout=Duration.seconds(20),
            memory_size=128,
            environment={
                "ENVIRONMENT": self.deployment_environment,
                "LOG_LEVEL": "DEBUG",
            },
            layers=[
                self.lambda_layer_fastapi,
            ],
        )

        # NOTE: If IAM-based based auth needed, update the "auth_type" to "AWS_IAM"
        self.lambda_function_url = self.lambda_fastapi.add_function_url(
            auth_type=aws_lambda.FunctionUrlAuthType.NONE
        )

    def generate_cloudformation_outputs(self):
        """
        Method to add the relevant CloudFormation outputs.
        """

        CfnOutput(
            self,
            "DeploymentEnvironment",
            value=self.deployment_environment,
            description="Deployment environment",
        )

        CfnOutput(
            self,
            "LambdaFunctionRootUrl",
            value=self.lambda_function_url.url,
            description="Root URL to invoke Lambda Function",
        )

        CfnOutput(
            self,
            "LambdaFunctionDocsUrl",
            value=f"{self.lambda_function_url.url}docs",
            description="Documentation URL to invoke Lambda Function",
        )
