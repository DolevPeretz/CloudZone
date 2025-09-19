from datetime import datetime
from app.logger import setup_logger
from app.validation import validate_id
from app.errors import AlreadyExists
from app.dynamodb_repo import CustomerDynamoDBRepository

logger = setup_logger("insert_id")
repo = CustomerDynamoDBRepository()

def handler(event, context):
    raw = event.get("id") if isinstance(event, dict) else None
    cid = validate_id(raw)

    try:
        repo.put(cid, {"created_at": datetime.utcnow().isoformat() + "Z"})
        logger.info(f"inserted id={cid}")
        return {"inserted": True}
    except AlreadyExists:
        logger.info(f"already_existed_at_put id={cid}")
        return {"inserted": False}

lambda_handler = handler
