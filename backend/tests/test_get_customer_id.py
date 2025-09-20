import pytest
from lambdas.get_customer_id import handler as get_module

class DummyRepoExistsTrue:
    def exists(self, _id): return True

class DummyRepoExistsFalse:
    def exists(self, _id): return False

class DummyRepoCrash:
    def exists(self, _id): raise RuntimeError("db error")

def _stub_validate_identity(x): return x
def _stub_validate_raises(_): raise ValueError("invalid id")

@pytest.fixture
def get_event_path():
    return {"pathParameters": {"id": "AB_123"}, "headers": {}, "queryStringParameters": None}

@pytest.fixture
def get_event_header():
    return {"pathParameters": None, "headers": {"ID": "AB_123"}, "queryStringParameters": None}

@pytest.fixture
def get_event_query():
    return {"pathParameters": None, "headers": {}, "queryStringParameters": {"id": "AB_123"}}

@pytest.fixture
def get_event_no_id():
    return {"pathParameters": None, "headers": {}, "queryStringParameters": None}

def test_get_exists_true(monkeypatch, get_event_path, extract_status_and_body):
    monkeypatch.setattr(get_module, "validate_id", _stub_validate_identity)
    monkeypatch.setattr(get_module, "repo", DummyRepoExistsTrue())

    resp = get_module.handler(get_event_path, context=None)
    status, body = extract_status_and_body(resp)

    assert status == 200
    assert body["exists"] is True
    assert body["id"] == "AB_123"

def test_get_exists_false(monkeypatch, get_event_header, extract_status_and_body):
    monkeypatch.setattr(get_module, "validate_id", _stub_validate_identity)
    monkeypatch.setattr(get_module, "repo", DummyRepoExistsFalse())

    resp = get_module.handler(get_event_header, context=None)
    status, body = extract_status_and_body(resp)

    assert status == 200
    assert body["exists"] is False
    assert body["id"] == "AB_123"

def test_get_from_querystring(monkeypatch, get_event_query, extract_status_and_body):
    monkeypatch.setattr(get_module, "validate_id", _stub_validate_identity)
    monkeypatch.setattr(get_module, "repo", DummyRepoExistsTrue())

    resp = get_module.handler(get_event_query, context=None)
    status, body = extract_status_and_body(resp)

    assert status == 200
    assert body["id"] == "AB_123"

def test_get_invalid_id(monkeypatch, get_event_path, extract_status_and_body):
    monkeypatch.setattr(get_module, "validate_id", _stub_validate_raises)
    monkeypatch.setattr(get_module, "repo", DummyRepoExistsTrue())

    resp = get_module.handler(get_event_path, context=None)
    status, body = extract_status_and_body(resp)

    assert status == 400
    assert "error" in body

def test_get_repo_crash(monkeypatch, get_event_path, extract_status_and_body):
    monkeypatch.setattr(get_module, "validate_id", _stub_validate_identity)
    monkeypatch.setattr(get_module, "repo", DummyRepoCrash())

    resp = get_module.handler(get_event_path, context=None)
    status, body = extract_status_and_body(resp)

    assert status == 400
    assert "error" in body

def test_get_missing_id(monkeypatch, get_event_no_id, extract_status_and_body):
    monkeypatch.setattr(get_module, "validate_id", _stub_validate_raises)
    monkeypatch.setattr(get_module, "repo", DummyRepoExistsTrue())

    resp = get_module.handler(get_event_no_id, context=None)
    status, body = extract_status_and_body(resp)

    assert status == 400
    assert "error" in body
