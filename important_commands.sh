#!/bin/bash

################################################################################
# PART 1: Configure NodeJs, Python and CDK libraries
################################################################################

# Install NodeJs and Python
# -->  https://nodejs.org/en/download/
# -->  https://www.python.org/downloads/

# Verify that NodeJs/npm is installed correctly
node --version
npm --version

# Verify that Python/pip is installed correctly
python --version || python3 --version
pip --version || pip3 --version

# Install AWS-CDK (on NodeJs)
sudo npm install -g aws-cdk

# Verify correct install of AWS-CDK
npm list --global | grep aws-cdk


################################################################################
# PART 2: Initial Project Setup (Only run these at the beginning)
################################################################################

# Configure AWS credentials (follow steps)
aws configure
# --> Alternative 1: Environment variables added to terminal session
# --> Alternative 2: AWS Cloud9 with the right permissions

# Bootstrap CDK (provision initial resources to work with CDK.. S3, roles, etc)
#! Change "ACCOUNT-NUMBER" and "REGION" to your needed values
cdk bootstrap aws://ACCOUNT-NUMBER/REGION

# Install poetry (for managing Python dependencies)
pip install poetry

# Install poetry dependencies for the virtual environment
poetry install


################################################################################
# PART 3: Main CDK and Python commands (most used)
################################################################################

# Activate Python virtual environment with Poetry tool
poetry shell

# Run unit tests
poe test-unit

# Deploy commands
export DEPLOYMENT_ENVIRONMENT=dev
cdk synth
cdk deploy


################################################################################
# PART 4: Other CDK usefull commands
################################################################################

# Help
cdk --help
cdk deploy --help

# Lists the stacks in the app
cdk list

# Synthesizes and prints the CloudFormation template for the specified stack(s)
cdk synthesize

# Deploys the CDK Toolkit staging stack (necessary resources in AWS account)
cdk bootstrap

# Deploys the specified stack(s)
cdk deploy

# Destroys the specified stack(s)
cdk destroy

# Compares the specified stack with the deployed stack or a local CloudFormation template
cdk diff

# Displays metadata about the specified stack
cdk metadata

# Creates a new CDK project in the current directory from a specified template
cdk init

# Manages cached context values
cdk context

# Opens the CDK API reference in your browser
cdk docs

# Checks your CDK project for potential problems
cdk doctor
