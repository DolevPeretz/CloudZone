import boto3
from botocore.exceptions import ClientError
from app.config import TABLE_NAME, AWS_REGION
from app.errors import AlreadyExists, NotFound

class CustomerDynamoDBRepository:
    def __init__(self, table_name: str | None = None, region_name: str | None = None, ddb=None):
        self._ddb = ddb or boto3.resource("dynamodb", region_name=region_name or AWS_REGION)
        self._table = self._ddb.Table(table_name or TABLE_NAME)

    def put(self, cid: str, attrs: dict | None = None) -> None:
        item = {"id": cid}
        if attrs:
            item.update(attrs)
        try:
            self._table.put_item(
                Item=item,
                ConditionExpression="attribute_not_exists(#id)",
                ExpressionAttributeNames={"#id": "id"},
            )
        except ClientError as ce:
            if ce.response.get("Error", {}).get("Code") == "ConditionalCheckFailedException":
                raise AlreadyExists("id already exists")
            raise


    def exists(self, cid: str) -> bool:
        res = self._table.get_item(Key={"id": cid}, ConsistentRead=True)
        return "Item" in res

    def delete(self, cid: str) -> None:
        try:
            self._table.delete_item(
                Key={"id": cid},
                ConditionExpression="attribute_exists(#id)",
                ExpressionAttributeNames={"#id": "id"},
            )
        except ClientError as ce:
            if ce.response.get("Error", {}).get("Code") == "ConditionalCheckFailedException":
                raise NotFound("id not found")
            raise
