# AWS CDK Python API Tutorial

This project demonstrates how to build and deploy a serverless REST API using:

- AWS CDK (Python)
- API Gateway
- AWS Lambda
- Amazon DynamoDB
- GitHub Actions
- GitHub OIDC Authentication (No AWS Access Keys)

---

# Architecture

```
GitHub
    │
    │ Push to dev
    ▼
GitHub Actions
    │
    │ OIDC Authentication
    ▼
GitHub Deployment Role
    │
    ▼
AWS CloudFormation
    │
    ├── API Gateway
    ├── Lambda
    └── DynamoDB
```

The Lambda function performs CRUD operations against DynamoDB through API Gateway.

---

# Prerequisites

Install:

- Python 3.12+
- Node.js
- AWS CLI
- AWS CDK CLI

Install CDK globally:

```bash
npm install -g aws-cdk
```

Create and activate a virtual environment.

Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows

```bat
python -m venv .venv
.venv\Scripts\activate.bat
```

Install Python dependencies.

```bash
pip install -r requirements.txt
```

---

# Bootstrap AWS CDK

CDK requires a bootstrap stack in each AWS account/region.

Run once:

```bash
cdk bootstrap
```

---

# Local Development

Useful commands:

```bash
cdk ls
```

Lists all stacks.

```bash
cdk synth
```

Generates the CloudFormation template.

```bash
cdk diff
```

Shows infrastructure changes.

```bash
cdk deploy
```

Deploys the stack.

```bash
cdk destroy
```

Deletes the stack.

---

# GitHub Deployment

Deployments are performed by GitHub Actions using **OIDC**.

No AWS Access Keys are stored in GitHub.

---

# Step 1 - Create GitHub OIDC Identity Provider

Open

```
AWS Console
→ IAM
→ Identity Providers
→ Add Provider
```

Provider Type

```
OpenID Connect
```

Provider URL

```
https://token.actions.githubusercontent.com
```

Audience

```
sts.amazonaws.com
```

This only needs to be created once per AWS account.

---

# Step 2 - Create IAM Deployment Roles

Create two IAM Roles.

```
github-dev-role
github-prod-role
```

Trusted Entity

```
Web Identity
```

Provider

```
token.actions.githubusercontent.com
```

Audience

```
sts.amazonaws.com
```

Repository

```
leojosefm/Iac_tutorial_aws
```

Branch

Development role

```
dev
```

Production role

```
main
```

---

# Step 3 - Permissions

For learning purposes attach:

```
AdministratorAccess
```

Later this can be replaced with a least-privilege policy.

---

# Step 4 - GitHub Environments

Create two GitHub Environments.

```
dev
prod
```

Repository

```
Settings
→ Environments
```

---

## Environment Secrets

### dev

```
DEV_ROLE_ARN
```

Example

```
arn:aws:iam::295263927767:role/github-dev-role
```

### prod

```
PROD_ROLE_ARN
```

Example

```
arn:aws:iam::295263927767:role/github-prod-role
```

Although the ARN is not considered sensitive, this project stores it as a secret because the repository is public.

---

## Environment Variables

### dev

```
AWS_REGION = us-east-1
STAGE = dev
```

### prod

```
AWS_REGION = us-east-1
STAGE = prod
```

---

# GitHub Workflows

Three workflows are used.

## 1. Dev Deployment

Trigger

```
Push to dev
```

Workflow

```
.github/workflows/dev-deploy.yml
```

Actions

- Authenticate using GitHub OIDC
- CDK Synth
- CDK Deploy

---

## 2. Production Diff

Trigger

```
Pull Request to main
```

Workflow

```
.github/workflows/prod-diff.yml
```

Actions

- Authenticate using GitHub OIDC
- CDK Diff

This allows infrastructure changes to be reviewed before deployment.

---

## 3. Production Deployment

Trigger

```
Manual (workflow_dispatch)
```

Workflow

```
.github/workflows/prod-deploy.yml
```

Actions

- Authenticate using GitHub OIDC
- CDK Deploy

Production deployments are intentionally manual.

---

# Deployment Flow

```
Developer
      │
      ▼
Push to dev
      │
      ▼
GitHub Actions
      │
      ▼
OIDC Authentication
      │
      ▼
github-dev-role
      │
      ▼
CloudFormation
      │
      ├── API Gateway
      ├── Lambda
      └── DynamoDB
```

Production follows the same process using the production role.

---

# Project Structure

```
.
├── app.py
├── aws_api
│   └── aws_api_stack.py
├── lambda
│   └── index.py
├── requirements.txt
├── cdk.json
└── .github
    └── workflows
        ├── dev-deploy.yml
        ├── prod-diff.yml
        └── prod-deploy.yml
```

---

# Resources Created

The stack deploys:

- API Gateway REST API
- Lambda Function
- DynamoDB Table
- Lambda Execution Role
- API Gateway Permissions
- CloudFormation Outputs

---

# Security

Authentication from GitHub to AWS uses OpenID Connect (OIDC).

Benefits:

- No long-lived AWS Access Keys
- Temporary AWS credentials
- Branch-specific deployment roles
- Separate permissions for Development and Production

This follows the current AWS recommended approach for GitHub Actions deployments.