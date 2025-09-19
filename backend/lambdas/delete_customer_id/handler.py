from app.http import resp
from app.logger import setup_logger
from app.validation import validate_id
from app.errors import NotFound
from app.dynamodb_repo import CustomerDynamoDBRepository

logger = setup_logger("delete_customer_id")
repo = CustomerDynamoDBRepository()

def _extract_id(event: dict) -> str | None:
    p = (event.get("pathParameters") or {}).get("id")
    if p: return p
    h = event.get("headers") or {}
    return h.get("id") or h.get("Id") or h.get("ID")

def handler(event, context):
    cid = _extract_id(event)
    try:
        cid = validate_id(cid)

        if not repo.exists(cid):
            logger.info(f"delete not_found: {cid}")
            return resp(404, {"error": f"Customer {cid} not found"})

        repo.delete(cid)
        logger.info(f"delete ok: {cid}")
        return resp(200, {"message": f"Customer {cid} deleted"})
    except NotFound:
        return resp(404, {"error": f"Customer {cid} not found"})
    except Exception:
        logger.error("delete failed")
        return resp(400, {"error": "invalid or missing id"})
