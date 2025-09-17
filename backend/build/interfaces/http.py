import json

def resp(status: int, body: dict):
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body)
    }

def parse_body(event):
    try:
        return json.loads(event.get("body") or "{}")
    except Exception:
        return {}
