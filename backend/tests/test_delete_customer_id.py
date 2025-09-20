import json
import pytest
from lambdas.delete_customer_id import handler as del_module

# ----- Self-contained un-wrapper (no conftest needed) -----
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

# ----- Dummy repos -----
class RepoDeleteOK:
    def exists(self, _id): return True
    def delete(self, _id): return None

class RepoNotFoundOnExists:
    def exists(self, _id): return False
    def delete(self, _id): raise AssertionError("should not be called")

class RepoDeleteRaisesNotFound:
    def exists(self, _id): return True
    def delete(self, _id): raise del_module.NotFound("no such customer")

class RepoCrash:
    def exists(self, _id): return True
    def delete(self, _id): raise RuntimeError("boom")

# ----- Stub validators -----
def _stub_validate_identity(x): return x
def _stub_validate_raises(_): raise ValueError("invalid id")

# ----- Event fixtures -----
@pytest.fixture
def del_event_path():
    return {"pathParameters": {"id": "AB_123"}, "headers": {}, "body": None}

@pytest.fixture
def del_event_header():
    return {"pathParameters": None, "headers": {"ID": "AB_123"}, "body": None}

@pytest.fixture
def del_event_no_id():
    return {"pathParameters": None, "headers": {}, "body": None}

# ----- Tests -----
def test_delete_success_via_path(monkeypatch, del_event_path):
    monkeypatch.setattr(del_module, "validate_id", _stub_validate_identity)
    monkeypatch.setattr(del_module, "repo", RepoDeleteOK())

    resp = del_module.handler(del_event_path, context=None)
    status, body = _unwrap(resp)

    assert status == 200
    assert "deleted" in body.get("message", "").lower()
    assert "ab_123" in body.get("message", "").lower()

def test_delete_success_via_header(monkeypatch, del_event_header):
    monkeypatch.setattr(del_module, "validate_id", _stub_validate_identity)
    monkeypatch.setattr(del_module, "repo", RepoDeleteOK())

    resp = del_module.handler(del_event_header, context=None)
    status, body = _unwrap(resp)

    assert status == 200
    assert "deleted" in body.get("message", "").lower()
    assert "ab_123" in body.get("message", "").lower()

def test_delete_not_found_when_exists_false(monkeypatch, del_event_path):
    monkeypatch.setattr(del_module, "validate_id", _stub_validate_identity)
    monkeypatch.setattr(del_module, "repo", RepoNotFoundOnExists())

    resp = del_module.handler(del_event_path, context=None)
    status, body = _unwrap(resp)

    assert status == 404
    assert "not found" in body.get("error", "").lower()

def test_delete_not_found_when_delete_raises(monkeypatch, del_event_path):
    monkeypatch.setattr(del_module, "validate_id", _stub_validate_identity)
    monkeypatch.setattr(del_module, "repo", RepoDeleteRaisesNotFound())

    resp = del_module.handler(del_event_path, context=None)
    status, body = _unwrap(resp)

    assert status == 404
    assert "not found" in body.get("error", "").lower()

def test_delete_invalid_id_returns_400(monkeypatch, del_event_path):
    monkeypatch.setattr(del_module, "validate_id", _stub_validate_raises)
    monkeypatch.setattr(del_module, "repo", RepoDeleteOK())

    resp = del_module.handler(del_event_path, context=None)
    status, body = _unwrap(resp)

    assert status == 400
    assert "invalid" in body.get("error", "").lower()

def test_delete_repo_crash_returns_400(monkeypatch, del_event_path):
    monkeypatch.setattr(del_module, "validate_id", _stub_validate_identity)
    monkeypatch.setattr(del_module, "repo", RepoCrash())

    resp = del_module.handler(del_event_path, context=None)
    status, body = _unwrap(resp)

    assert status == 400
    assert "invalid" in body.get("error", "").lower() or "error" in body
