from app.logger import setup_logger
from app.validation import validate_id
from app.dynamodb_repo import CustomerDynamoDBRepository

logger = setup_logger("validate_exists")
repo = CustomerDynamoDBRepository()

def _extract_id(event: dict) -> str | None:
    if not isinstance(event, dict):
        return None
    if "id" in event:
        return event["id"]
    d = event.get("detail") or {} 
    if "id" in d:
        return d["id"]
    p = (event.get("pathParameters") or {}).get("id") 
    if p:
        return p
    h = event.get("headers") or {}  
    return h.get("id") or h.get("Id") or h.get("ID")

def handler(event, context):
    cid = validate_id(_extract_id(event))
    exists = repo.exists(cid)
    logger.info(f"validate_exists ok: {cid}, exists={exists}")
    return {"exists": exists}

lambda_handler = handler
