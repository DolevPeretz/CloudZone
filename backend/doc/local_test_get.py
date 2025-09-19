import os, json, sys
from moto import mock_aws
import boto3

# לאפשר imports מהשורש
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

os.environ["AWS_DEFAULT_REGION"] = "eu-central-1"
os.environ["TABLE_NAME"] = "customer_ids"

from lambdas.get_customer_id.handler import handler

@mock_aws
def run():
    ddb = boto3.client("dynamodb", region_name="eu-central-1")
    ddb.create_table(
        TableName="customer_ids",
        KeySchema=[{"AttributeName":"id","KeyType":"HASH"}],
        AttributeDefinitions=[{"AttributeName":"id","AttributeType":"S"}],
        BillingMode="PAY_PER_REQUEST",
    )
    ddb.put_item(TableName="customer_ids", Item={"id": {"S": "abc-123"}})

    event = {"queryStringParameters": {"id": "abc-123"}}
    res = handler(event, None)
    print(json.dumps(res, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    run()
