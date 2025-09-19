# app/http.py
import json, base64
from typing import Any, Dict, Optional

CORS_HEADERS: Dict[str, str] = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
    "Access-Control-Allow-Methods": "GET,PUT,DELETE,POST,OPTIONS",  
    "Content-Type": "application/json", 
}

def resp(status: int, payload: Any, headers: Optional[Dict[str, str]] = None):
    return {
        "statusCode": status,
        "headers": {**CORS_HEADERS, **(headers or {})},
        "body": json.dumps(payload),
    }

def parse_body(event) -> dict:
    raw = event.get("body") or "{}"
    if event.get("isBase64Encoded"):
        try:
            raw = base64.b64decode(raw).decode("utf-8", errors="ignore")
        except Exception:
            return {}
    try:
        return json.loads(raw)
    except Exception:
        return {}
