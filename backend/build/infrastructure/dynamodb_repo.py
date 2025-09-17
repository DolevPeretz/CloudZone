import boto3
from botocore.exceptions import ClientError
from app.ports.customer_repo import ICustomerRepository
from app.domain.entities import CustomerId
from app.domain.errors import AlreadyExists
from infrastructure.config import TABLE_NAME


_dynamodb = boto3.resource("dynamodb")
_table = _dynamodb.Table(TABLE_NAME)

class CustomerDynamoDBRepository(ICustomerRepository):
    def put(self, cid: CustomerId) -> None:
        try:
            _table.put_item(
                Item={"id": cid.value},
                ConditionExpression="attribute_not_exists(#id)",
                ExpressionAttributeNames={"#id": "id"}
            )
        except ClientError as ce:
            if ce.response.get("Error", {}).get("Code") == "ConditionalCheckFailedException":
                raise AlreadyExists("id already exists")
            raise

    def exists(self, cid: CustomerId) -> bool:
        res = _table.get_item(Key={"id": cid.value})
        return "Item" in res

    def delete(self, cid: CustomerId) -> None:
        _table.delete_item(Key={"id": cid.value})


# חיבור לדיינמו
          