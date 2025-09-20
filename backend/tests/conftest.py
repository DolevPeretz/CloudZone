# backend/tests/conftest.py
import json
import pytest

# === Event fixtures לדוגמה (אם כבר קיימים, אפשר להשאיר/לא לשכפל) ===
@pytest.fixture
def put_event_path_ok():
    return {"pathParameters": {"id": "AB_123"}, "headers": {}, "body": None}

@pytest.fixture
def put_event_header_ok():
    return {"pathParameters": None, "headers": {"ID": "AB_123"}, "body": None}

@pytest.fixture
def put_event_no_id():
    return {"pathParameters": None, "headers": {}, "body": None}

# === helper שמפרק את התגובה ===
def _extract_status_and_body(resp):
    # מחזיר (status_code, body_dict)
    if isinstance(resp, dict):
        status = resp.get("statusCode") or resp.get("status") or resp.get("code")
        body = resp.get("body")
        if isinstance(body, str):
            try:
                body = json.loads(body)
            except Exception:
                body = {"body": body}
        elif body is None:
            msg = resp.get("message")
            body = {"message": msg} if msg else {}
        return status, body
    if isinstance(resp, tuple) and len(resp) >= 2:
        status, body = resp[0], resp[1]
        if isinstance(body, str):
            try:
                body = json.loads(body)
            except Exception:
                body = {"body": body}
        return status, body
    return None, {"_raw": resp}

@pytest.fixture
def extract_status_and_body():
    return _extract_status_and_body
