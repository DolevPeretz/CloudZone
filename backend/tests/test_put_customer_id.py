import json
import types
import pytest

from lambdas.put_customer_id.handler import handler as put_handler

from app.errors import InvalidCustomerId, AlreadyExists

def _event(cid):
    return {
        "resource": "/customers/{id}",
        "pathParameters": {"id": cid},
        "httpMethod": "PUT",
        "headers": {},
        "body": None,
        "isBase64Encoded": False,
    }

def test_put_ok(monkeypatch):
    monkeypatch.setattr("lambdas.put_customer_id.handler.validate_id", lambda x: x)

    class RepoOK:
        def put(self, cid): 
            assert cid == "abc123"
            return None

    monkeypatch.setattr("lambdas.put_customer_id.handler.repo", RepoOK())

    resp = put_handler(_event("abc123"), None)
    assert resp["statusCode"] == 201
    body = json.loads(resp["body"])
    assert body == {"message": "created", "id": "abc123"}

def test_put_invalid_id(monkeypatch):
    def bad(_): 
        raise InvalidCustomerId("bad id")
    monkeypatch.setattr("lambdas.put_customer_id.handler.validate_id", bad)

    class RepoDummy:
        def put(self, cid): 
            raise AssertionError("should not be called")
    monkeypatch.setattr("lambdas.put_customer_id.handler.repo", RepoDummy())

    resp = put_handler(_event(""), None)
    assert resp["statusCode"] == 400
    assert "error" in json.loads(resp["body"])

def test_put_conflict(monkeypatch):
    monkeypatch.setattr("lambdas.put_customer_id.handler.validate_id", lambda x: x)

    class RepoConflict:
        def put(self, cid):
            raise AlreadyExists(f"{cid} exists")
    monkeypatch.setattr("lambdas.put_customer_id.handler.repo", RepoConflict())

    resp = put_handler(_event("dup-1"), None)
    assert resp["statusCode"] == 409

def test_put_internal_error(monkeypatch):
    monkeypatch.setattr("lambdas.put_customer_id.handler.validate_id", lambda x: x)

    class RepoBoom:
        def put(self, cid):
            raise RuntimeError("ddb down")
    monkeypatch.setattr("lambdas.put_customer_id.handler.repo", RepoBoom())

    resp = put_handler(_event("x1"), None)
    assert resp["statusCode"] == 500
