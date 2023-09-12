# AWS PREREQUISITES FOR THE GITHUB ACTIONS CI/CD PIPELINE

Inspired on:

- https://github.com/aws-actions/configure-aws-credentials/tree/main/examples

The CI/CD uses aws-action `configure-aws-credentials` with OIDC federation. Prior to using this example project, the user needs to deploy the [github-actions-oidc-federation-and-role](github-actions-oidc-federation-and-role.yml) CloudFormation template in the AWS account they want to deploy the solution. Specify the GitHub Organization name, repository name, and the specific branch you want to deploy on.

To use the example you will need to set the following GitHub Action Secrets:

| Secret Key      | Used With                 | Description              |
| --------------- | ------------------------- | ------------------------ |
| AWS_ACCOUNT_ID  | configure-aws-credentials | The AWS account ID       |
| AWS_DEPLOY_ROLE | configure-aws-credentials | The name of the IAM role |
