from interfaces.http import resp
from infrastructure.dynamodb_repo import CustomerDynamoDBRepository
from app.use_cases.get_customer_id import check_customer_exists
from app.domain.errors import InvalidCustomerId

_repo = CustomerDynamoDBRepository()

def handler(event, context):
    path_params = event.get("pathParameters") or {}
    cid = path_params.get("id")

    if not cid:
        return resp(400, {"error": "missing id"})

    try:
        exists = check_customer_exists(_repo, cid)
        return resp(200, {"exists": exists, "id": cid})
    except InvalidCustomerId as e:
        return resp(400, {"error": str(e)})
    except Exception:
        return resp(500, {"error": "internal"})
