import json
import pytest
from lambdas.submit_customer_id import handler as submit_module

def _unwrap(resp):
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

class FakeEvents:
    def __init__(self):
        self.calls = []
    def put_events(self, Entries):
        self.calls.append({"Entries": Entries})
        return {"FailedEntryCount": 0, "Entries": [{"EventId": "evt-1"}]}

def _stub_validate_identity(x): return x
def _stub_validate_raises(_): raise ValueError("invalid id")

@pytest.fixture
def ev_body_json():
    return {
        "body": json.dumps({"id": "AB_123"}),
        "pathParameters": None,
        "headers": {},
    }

@pytest.fixture
def ev_path():
    return {
        "body": None,
        "pathParameters": {"id": "AB_123"},
        "headers": {},
    }

@pytest.fixture
def ev_header():
    return {
        "body": None,
        "pathParameters": None,
        "headers": {"ID": "AB_123"},
    }

@pytest.fixture
def ev_no_id():
    return {"body": None, "pathParameters": None, "headers": {}}

def test_submit_from_body_json(monkeypatch, ev_body_json):
    monkeypatch.setattr(submit_module, "EVENT_BUS_NAME", "bus-x")
    monkeypatch.setattr(submit_module, "EVENT_SOURCE", "src-x")
    monkeypatch.setattr(submit_module, "EVENT_DETAIL_TYPE", "detail-x")

    fake = FakeEvents()
    monkeypatch.setattr(submit_module, "events", fake)
    monkeypatch.setattr(submit_module, "validate_id", _stub_validate_identity)

    resp = submit_module.handler(ev_body_json, context=None)
    status, body = _unwrap(resp)

    assert status == 202
    assert body["status"] == "accepted"
    assert body["id"] == "AB_123"

    assert len(fake.calls) == 1
    call = fake.calls[0]["Entries"][0]
    assert call["EventBusName"] == "bus-x"
    assert call["Source"] == "src-x"
    assert call["DetailType"] == "detail-x"
    detail = json.loads(call["Detail"])
    assert detail == {"id": "AB_123"}

def test_submit_from_path(monkeypatch, ev_path):
    monkeypatch.setattr(submit_module, "EVENT_BUS_NAME", "bus-y")
    monkeypatch.setattr(submit_module, "EVENT_SOURCE", "src-y")
    monkeypatch.setattr(submit_module, "EVENT_DETAIL_TYPE", "detail-y")

    fake = FakeEvents()
    monkeypatch.setattr(submit_module, "events", fake)
    monkeypatch.setattr(submit_module, "validate_id", _stub_validate_identity)

    resp = submit_module.handler(ev_path, context=None)
    status, body = _unwrap(resp)

    assert status == 202
    assert body["id"] == "AB_123"
    call = fake.calls[0]["Entries"][0]
    assert call["EventBusName"] == "bus-y"
    assert call["Source"] == "src-y"
    assert call["DetailType"] == "detail-y"
    assert json.loads(call["Detail"]) == {"id": "AB_123"}

def test_submit_from_header(monkeypatch, ev_header):
    monkeypatch.setattr(submit_module, "EVENT_BUS_NAME", "bus-z")
    monkeypatch.setattr(submit_module, "EVENT_SOURCE", "src-z")
    monkeypatch.setattr(submit_module, "EVENT_DETAIL_TYPE", "detail-z")

    fake = FakeEvents()
    monkeypatch.setattr(submit_module, "events", fake)
    monkeypatch.setattr(submit_module, "validate_id", _stub_validate_identity)

    resp = submit_module.handler(ev_header, context=None)
    status, body = _unwrap(resp)

    assert status == 202
    assert body["id"] == "AB_123"
    call = fake.calls[0]["Entries"][0]
    assert call["EventBusName"] == "bus-z"
    assert call["Source"] == "src-z"
    assert call["DetailType"] == "detail-z"
    assert json.loads(call["Detail"]) == {"id": "AB_123"}

def test_submit_invalid_id_returns_400(monkeypatch, ev_header):
    fake = FakeEvents()
    monkeypatch.setattr(submit_module, "events", fake)
    monkeypatch.setattr(submit_module, "validate_id", _stub_validate_raises)

    resp = submit_module.handler(ev_header, context=None)
    status, body = _unwrap(resp)
    assert status == 400
    assert "error" in body
    assert len(fake.calls) == 0

def test_lambda_handler_alias(monkeypatch, ev_path):
    monkeypatch.setattr(submit_module, "EVENT_BUS_NAME", "bus-a")
    monkeypatch.setattr(submit_module, "EVENT_SOURCE", "src-a")
    monkeypatch.setattr(submit_module, "EVENT_DETAIL_TYPE", "detail-a")

    fake = FakeEvents()
    monkeypatch.setattr(submit_module, "events", fake)
    monkeypatch.setattr(submit_module, "validate_id", _stub_validate_identity)

    resp = submit_module.lambda_handler(ev_path, context=None)
    status, body = _unwrap(resp)

    assert status == 202
    assert body["id"] == "AB_123"
    assert len(fake.calls) == 1
