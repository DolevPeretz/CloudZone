from app.logger import setup_logger

logger = setup_logger("log_event")

def _get(d: dict | None, path: list[str], default=None):
    cur = d if isinstance(d, dict) else None
    for k in path:
        if not isinstance(cur, dict):
            return default
        cur = cur.get(k)
    return cur if cur is not None else default

def handler(event, context):
    cid = _get(event, ["id"]) or _get(event, ["detail", "id"])

    payload = {
        "level": "INFO",
        "msg": "workflow_log",
        "customer_id": cid,
        "exists": _get(event, ["validation", "exists"]),
        "inserted": _get(event, ["insert", "inserted"]),
        "request_id": getattr(context, "aws_request_id", None),
    }

    import json
    logger.info(json.dumps(payload))
    return {"logged": True}

lambda_handler = handler
