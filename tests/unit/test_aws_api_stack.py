import aws_cdk as core
import aws_cdk.assertions as assertions

from aws_api.aws_api_stack import AwsApiStack

# example tests. To run these tests, uncomment this file along with the example
# resource in aws_api/aws_api_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = AwsApiStack(app, "aws-api")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
