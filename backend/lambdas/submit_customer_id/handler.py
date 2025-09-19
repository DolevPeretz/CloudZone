from json import loads, dumps
import boto3
from app.logger import setup_logger
from app.http import resp
from app.validation import validate_id
from app.config import AWS_REGION, EVENT_BUS_NAME, EVENT_SOURCE, EVENT_DETAIL_TYPE

logger = setup_logger("submit_customer_id")
events = boto3.client("events", region_name=AWS_REGION)

def _extract_id(event: dict) -> str | None:
    body = event.get("body")
    if isinstance(body, str):
        try:
            body = loads(body)
        except Exception:
            body = None
    if isinstance(body, dict) and "id" in body:
        return body["id"]
    p = (event.get("pathParameters") or {}).get("id")
    if p: 
        return p
    h = event.get("headers") or {}
    return h.get("id") or h.get("Id") or h.get("ID")

def handler(event, context):
    try:
        cid = validate_id(_extract_id(event))

        events.put_events(Entries=[{
            "EventBusName": EVENT_BUS_NAME,              
            "Source":      EVENT_SOURCE,                
            "DetailType":  EVENT_DETAIL_TYPE,            
            "Detail":      dumps({"id": cid})
        }])

        logger.info(f"submitted id={cid}")
        return resp(202, {"status": "accepted", "id": cid})
    except Exception as e:
        logger.error(f"submit failed: {e}")
        return resp(400, {"error": "invalid or missing id"})

lambda_handler = handler
