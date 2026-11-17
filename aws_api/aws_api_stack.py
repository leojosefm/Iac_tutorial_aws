from aws_cdk import (
    Stack,
    RemovalPolicy,       # Controls what happens to resources when you delete the stack
    CfnOutput,           # Prints useful values (like URLs) after deployment
    aws_dynamodb as dynamodb,
)
from constructs import Construct  # The base class for all CDK resources

class CrudApiStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        # Pass any extra settings (like AWS region) to the parent Stack class
        super().__init__(scope, id, **kwargs)

        # --- DATABASE ---
        # DynamoDB is a NoSQL database. Each item needs a unique "partition key."
        # Think of it like a Python dictionary: the partition key is the dict key,
        # and the item is the dict value.
        items_table = dynamodb.Table(
            self,
            "ItemsTable",
            partition_key=dynamodb.Attribute(
                name="id",                          # Each item gets a unique "id" field
                type=dynamodb.AttributeType.STRING,  # The id will be a string (like a UUID)
            ),
            # PAY_PER_REQUEST means you pay per read/write, not for reserved capacity.
            # At tutorial traffic levels, this costs fractions of a penny.
            # For production with unpredictable traffic, it's also the safer choice.
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            # DESTROY means "delete this table when I run cdk destroy."
            # The default is RETAIN, which keeps the table (and the bill) even after
            # you delete the stack. For a learning project, DESTROY is what you want.
            removal_policy=RemovalPolicy.DESTROY,
        )

        # --- OUTPUTS ---
        CfnOutput(
            self,
            "TableName",
            value=items_table.table_name,
            description="DynamoDB table name",
        )