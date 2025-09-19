from app.http import resp
from app.logger import setup_logger
from app.validation import validate_id
from app.dynamodb_repo import CustomerDynamoDBRepository

logger = setup_logger("get_customer_id")
repo = CustomerDynamoDBRepository()

def _extract_id(event: dict) -> str | None:
    p = (event.get("pathParameters") or {}).get("id")
    if p: return p
    h = event.get("headers") or {}
    p = h.get("id") or h.get("Id") or h.get("ID")
    if p: return p
    q = event.get("queryStringParameters") or {}
    return q.get("id")

def handler(event, context):
    cid = _extract_id(event)
    try:
        cid = validate_id(cid)
        exists = repo.exists(cid)
        logger.info(f"get ok: {cid}, exists={exists}")
        return resp(200, {"exists": exists, "id": cid})
    except Exception:
        logger.error("get failed")
        return resp(400, {"error": "invalid or missing id"})
