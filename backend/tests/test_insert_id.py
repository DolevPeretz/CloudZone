import json
import pytest
from datetime import datetime, timezone
from lambdas.insert_id import handler as insert_module

class RepoPutOK:
    def __init__(self):
        self.calls = []

    def put(self, cid, attrs=None):
        self.calls.append((cid, attrs or {}))
        return None

class RepoPutExists:
    def put(self, cid, attrs=None):
        raise insert_module.AlreadyExists("exists")

def _stub_validate_identity(x):  
    return x

def _stub_validate_raises(_):  
    raise ValueError("invalid id")

class _FixedDateTime:
    @classmethod
    def utcnow(cls):
        return datetime(2025, 9, 1, 12, 34, 56, tzinfo=timezone.utc).replace(tzinfo=None)

def test_insert_success_inserts_with_created_at(monkeypatch):
    monkeypatch.setattr(insert_module, "validate_id", _stub_validate_identity)
    monkeypatch.setattr(insert_module, "datetime", _FixedDateTime)
    repo = RepoPutOK()
    monkeypatch.setattr(insert_module, "repo", repo)

    event = {"id": "AB_123"}
    resp = insert_module.handler(event, context=None)
    assert resp == {"inserted": True}

    assert len(repo.calls) == 1
    cid, attrs = repo.calls[0]
    assert cid == "AB_123"
    assert isinstance(attrs, dict) and "created_at" in attrs
    assert attrs["created_at"] == "2025-09-01T12:34:56Z"
    assert attrs["created_at"].endswith("Z")

def test_insert_already_exists_returns_false(monkeypatch):
    monkeypatch.setattr(insert_module, "validate_id", _stub_validate_identity)
    monkeypatch.setattr(insert_module, "datetime", _FixedDateTime)
    monkeypatch.setattr(insert_module, "repo", RepoPutExists())

    event = {"id": "AB_123"}
    resp = insert_module.handler(event, context=None)
    assert resp == {"inserted": False}

def test_insert_invalid_id_raises(monkeypatch):
    monkeypatch.setattr(insert_module, "validate_id", _stub_validate_raises)
    monkeypatch.setattr(insert_module, "repo", RepoPutOK())
    monkeypatch.setattr(insert_module, "datetime", _FixedDateTime)

    with pytest.raises(Exception):
        insert_module.handler({"id": "!!bad"}, context=None)

def test_insert_event_not_dict_raises(monkeypatch):
    monkeypatch.setattr(insert_module, "validate_id", _stub_validate_raises)
    monkeypatch.setattr(insert_module, "repo", RepoPutOK())
    monkeypatch.setattr(insert_module, "datetime", _FixedDateTime)

    with pytest.raises(Exception):
        insert_module.handler("not-a-dict", context=None)

def test_lambda_handler_alias(monkeypatch):
    monkeypatch.setattr(insert_module, "validate_id", _stub_validate_identity)
    monkeypatch.setattr(insert_module, "datetime", _FixedDateTime)
    repo = RepoPutOK()
    monkeypatch.setattr(insert_module, "repo", repo)

    resp = insert_module.lambda_handler({"id": "AB_123"}, context=None)
    assert resp == {"inserted": True}
    assert len(repo.calls) == 1
