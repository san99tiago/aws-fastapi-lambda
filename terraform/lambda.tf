data "aws_iam_policy_document" "lambda_trust_policy" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "lambda_role" {
  name               = "${var.main_resources_name}-role-${var.environment}"
  assume_role_policy = data.aws_iam_policy_document.lambda_trust_policy.json
}

# Add "AWSLambdaBasicExecutionRole" to the role for the Lambda Function
resource "aws_iam_role_policy_attachment" "lambda_basic_execution_role" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Create ZIP file for the source code at deployment time
data "archive_file" "lambda_source_package" {
  type        = "zip"
  source_dir  = "${local.src_root_path}/lambdas"
  output_path = "${local.src_root_path}/lambda_package.zip"
}

# Lambda Layer Install (Python dependencies)
resource "null_resource" "lambda_layer_install_deps" {
  provisioner "local-exec" {
    command     = "make install"
    working_dir = local.root_path
  }

  # Enforce to always execute the command
  triggers = {
    always_run = "${timestamp()}"
  }
}

# Create ZIP file for Lambda Layer (Python dependencies)
data "archive_file" "lambda_layer_package" {
  type        = "zip"
  source_dir  = "${local.lambda_layers_root_path}/fastapi/modules"
  output_path = "${local.lambda_layers_root_path}/fastapi/modules/lambda_layer_package.zip"

  depends_on = [null_resource.lambda_layer_install_deps]
}

# Lambda Layer
resource "aws_lambda_layer_version" "lambda_layer" {
  filename                 = "${local.lambda_layers_root_path}/fastapi/modules/lambda_layer_package.zip"
  layer_name               = "${var.main_resources_name}-layer"
  compatible_runtimes      = ["python3.12"]
  compatible_architectures = ["x86_64"]
  source_code_hash         = data.archive_file.lambda_layer_package.output_base64sha256 # Enforce re-deploy on changes

  depends_on = [data.archive_file.lambda_layer_package]

}

resource "aws_lambda_function" "lambda" {
  function_name    = "${var.main_resources_name}-${var.environment}"
  filename         = "${local.src_root_path}/lambda_package.zip"
  handler          = "api/main.handler"
  role             = aws_iam_role.lambda_role.arn
  runtime          = "python3.12"
  timeout          = 20
  architectures    = ["x86_64"]
  layers           = [aws_lambda_layer_version.lambda_layer.arn]
  source_code_hash = data.archive_file.lambda_source_package.output_base64sha256 # Enforce re-deploy on changes


  environment {
    variables = {
      ENVIRONMENT = var.environment
    }
  }

  depends_on = [
    data.archive_file.lambda_source_package,
    data.archive_file.lambda_layer_package,
  ]

}

resource "aws_lambda_function_url" "lambda_url" {
  function_name      = aws_lambda_function.lambda.function_name
  authorization_type = "NONE"
}
