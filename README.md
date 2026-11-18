# AWS CDK Python Serverless REST API

This project demonstrates how to build and deploy a serverless REST API on AWS using Infrastructure as Code (IaC).

## Technologies

- AWS CDK (Python)
- Amazon API Gateway
- AWS Lambda
- Amazon DynamoDB
- AWS CloudFormation
- GitHub Actions

---

# Architecture

```
Client
   │
   ▼
API Gateway
   │
   ▼
Lambda
   │
   ▼
DynamoDB
```

Infrastructure is provisioned using AWS CDK and deployed through GitHub Actions.

---

# Prerequisites

Install:

- Python 3.12+
- Node.js
- AWS CLI
- AWS CDK CLI

Install CDK:

```bash
npm install -g aws-cdk
```

Create a virtual environment.

Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows

```bat
python -m venv .venv
.venv\Scripts\activate.bat
```

Install dependencies.

```bash
pip install -r requirements.txt
```

---

# Bootstrap CDK

Bootstrap the AWS account once per region.

```bash
cdk bootstrap
```

---

# Local Development

List stacks

```bash
cdk ls
```

Generate CloudFormation template

```bash
cdk synth
```

Preview infrastructure changes

```bash
cdk diff
```

Deploy

```bash
cdk deploy
```

Destroy

```bash
cdk destroy
```

---

# GitHub Environments

Two GitHub Environments are used.

- dev
- prod

Each environment contains:

| Variable | Value |
|----------|-------|
| AWS_REGION | us-east-1 |
| STAGE | dev / prod |

Required GitHub Secrets:

| Secret |
|---------|
| AWS_ACCESS_KEY_ID |
| AWS_SECRET_ACCESS_KEY |

---

# CI/CD

## Development

Trigger:

```
Push to dev
```

Pipeline:

```
CDK Synth
↓
CDK Diff
↓
CDK Deploy
```

---

## Promote to Production

Trigger:

```
Manual
```

This workflow merges the `dev` branch into `main`.

---

## Production Validation

Trigger:

```
Push to main
```

Pipeline:

```
CDK Synth
↓
CDK Diff
```

This validates infrastructure changes before deployment.

---

## Production Deployment

Trigger:

```
Manual
```

Pipeline:

```
CDK Deploy
```

---

# Deployment Flow

```
Push to dev
      │
      ▼
DEV Deployment
      │
      ▼
Manual Promotion
(dev → main)
      │
      ▼
Production Diff
      │
      ▼
Manual Production Deployment
```

---

# Project Structure

```
.
├── app.py
├── aws_api/
│   └── aws_api_stack.py
├── lambda/
│   └── index.py
├── requirements.txt
├── cdk.json
└── .github/
    └── workflows/
        ├── dev-deploy.yml
        ├── promote-dev-to-main.yml
        ├── prod-diff.yml
        └── prod-deploy.yml
```

---

# AWS Resources

The CDK stack creates:

- API Gateway REST API
- Lambda Function
- DynamoDB Table
- IAM Roles and Policies
- CloudFormation Outputs

---

# Future Improvements

- Replace IAM Access Keys with GitHub OIDC authentication
- Least-privilege IAM policies
- Automated testing
- Multi-account deployments
- Monitoring with CloudWatch