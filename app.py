#!/usr/bin/env python3
import os

import aws_cdk as cdk

from aws_api.aws_api_stack import AwsApiStack


app = cdk.App()

stage = app.node.try_get_context("stage") or "dev"

AwsApiStack(app, f"AwsApiStack-{stage}", stack_name=f"aws-api-{stage}")

app.synth()
