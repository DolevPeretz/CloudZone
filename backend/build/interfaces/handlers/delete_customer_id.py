from interfaces.http import resp
from infrastructure.dynamodb_repo import CustomerDynamoDBRepository
from app.use_cases.delete_customer_id import delete_customer_id as uc_delete
from app.domain.errors import InvalidCustomerId

_repo = CustomerDynamoDBRepository()

def handler(event, context):
    path_params = event.get("pathParameters") or {}
    cid = path_params.get("id")

    if not cid:
        return resp(400, {"error": "missing id"})

    try:
        uc_delete(_repo, cid)
        return resp(200, {"message": "deleted", "id": cid})
    except InvalidCustomerId as e:
        return resp(400, {"error": str(e)})
    except Exception:
        return resp(500, {"error": "internal"})
