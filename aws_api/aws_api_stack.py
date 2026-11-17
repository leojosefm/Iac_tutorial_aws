from aws_cdk import (
    Stack,
    RemovalPolicy,
    CfnOutput,
    Duration,                # For setting timeouts
    aws_dynamodb as dynamodb,
    aws_lambda as _lambda,   # "lambda" is a reserved word in Python, so CDK uses "_lambda"
    aws_apigateway as apigw
)
from constructs import Construct


class AwsApiStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)


        # --- DATABASE ---
        items_table = dynamodb.Table(
            self,
            "ItemsTable",
            partition_key=dynamodb.Attribute(
                name="id",
                type=dynamodb.AttributeType.STRING,
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY, # For stateful resources
        )


        # --- LAMBDA FUNCTION ---
        # Lambda runs your code without you managing a server.
        # "index.handler" means: in index.py, call the function named handler.
        # CDK zips the "lambda" folder and uploads it to AWS during deployment.
        api_handler = _lambda.Function(
            self,
            "ApiHandler",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="index.handler",
            code=_lambda.Code.from_asset("lambda"),
            environment={
                "TABLE_NAME": items_table.table_name,
            },
            timeout=Duration.seconds(10),
            memory_size=128,
        )


        # --- PERMISSIONS ---
        # Grant the Lambda function permission to read/write the table
        items_table.grant_read_write_data(api_handler)


        # --- API GATEWAY ---
        api = apigw.RestApi(
            self,
            "ItemsApi",
            rest_api_name="Item Service API",
            description="API for items, built with CDK",
        )


        # LambdaIntegration tells API Gateway: "forward requests to this function"
        items_integration = apigw.LambdaIntegration(api_handler)


        # --- ROUTES ---
        # Like defining routes in Flask or Express
        items_resource = api.root.add_resource("items") # base_url/items
        items_resource.add_method("GET", items_integration)    # List all items
        items_resource.add_method("POST", items_integration)   # Create item


        single_item = items_resource.add_resource("{id}")      # /items/{id}
        single_item.add_method("GET", items_integration)       # Get one item
        single_item.add_method("PUT", items_integration)       # Update item
        single_item.add_method("DELETE", items_integration)    # Delete item


        # --- OUTPUTS ---
        CfnOutput(
            self,
            "ApiEndpoint",
            value=api.url,
            description="API Gateway endpoint URL",
        )

        CfnOutput(
                self,
                "LambdaArn",
                value=api_handler.function_arn,
                description="Lambda ARN",
            )

        CfnOutput(
            self,
            "TableName",
            value=items_table.table_name,
            description="DynamoDB table name",
        )
