from app.http import resp
from app.logger import setup_logger
from app.validation import validate_id
from app.errors import InvalidCustomerId, AlreadyExists
from app.dynamodb_repo import CustomerDynamoDBRepository

logger = setup_logger("put_customer_id")
repo = CustomerDynamoDBRepository()

def handler(event, context):
    cid = (event.get("pathParameters") or {}).get("id")
    if not cid:
        h = event.get("headers") or {}
        cid = h.get("id") or h.get("Id") or h.get("ID")

    try:
        cid = validate_id(cid)
        repo.put(cid)
        logger.info(f"put ok: {cid}")
        return resp(201, {"message": "created", "id": cid})
    except InvalidCustomerId as e:
        return resp(400, {"error": str(e)})
    except AlreadyExists as e:
        return resp(409, {"error": str(e)})
    except Exception:
        return resp(500, {"error": "internal"})
