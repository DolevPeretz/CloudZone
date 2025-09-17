from interfaces.http import resp
from infrastructure.dynamodb_repo import CustomerDynamoDBRepository
from app.use_cases.add_customer_id import add_customer_id
from app.domain.errors import InvalidCustomerId, AlreadyExists

_repo = CustomerDynamoDBRepository()

def handler(event, context):
    path_params = event.get("pathParameters") or {}
    cid = path_params.get("id")

    if not cid:
        return resp(400, {"error": "missing id"})

    try:
        add_customer_id(_repo, cid)
        return resp(201, {"message": "created", "id": cid})
    except InvalidCustomerId as e:
        return resp(400, {"error": str(e)})
    except AlreadyExists as e:
        return resp(409, {"error": str(e)})
    except Exception:
        return resp(500, {"error": "internal"})
