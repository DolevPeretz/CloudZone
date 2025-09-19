import os, json, sys
from moto import mock_aws
import boto3

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

os.environ["AWS_DEFAULT_REGION"] = "eu-central-1"
os.environ["TABLE_NAME"] = "customer_ids"

from lambdas.delete_customer_id.handler import handler as delete_handler
from lambdas.get_customer_id.handler import handler as get_handler

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

    delete_event = {"pathParameters": {"id": "abc-123"}}
    res_del = delete_handler(delete_event, None)
    print("DELETE response:\n", json.dumps(res_del, ensure_ascii=False, indent=2))

    get_event = {"queryStringParameters": {"id": "abc-123"}}
    res_get = get_handler(get_event, None)
    print("GET after delete:\n", json.dumps(res_get, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    run()
