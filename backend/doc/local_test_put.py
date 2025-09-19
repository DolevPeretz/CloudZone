import os, json, sys
from moto import mock_aws
import boto3

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

os.environ["AWS_DEFAULT_REGION"] = "eu-central-1"
os.environ["TABLE_NAME"] = "customer_ids"

from lambdas.put_customer_id.handler import handler

@mock_aws
def run():
    ddb = boto3.client("dynamodb", region_name="eu-central-1")
    ddb.create_table(
        TableName="customer_ids",
        KeySchema=[{"AttributeName":"id","KeyType":"HASH"}],
        AttributeDefinitions=[{"AttributeName":"id","AttributeType":"S"}],
        BillingMode="PAY_PER_REQUEST",
    )

    event = {"pathParameters": {"id": "abc-123"}}
    res = handler(event, None)
    print(json.dumps(res, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    run()
