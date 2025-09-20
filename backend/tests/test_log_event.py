import json
import pytest
from types import SimpleNamespace
from lambdas.log_event import handler as log_module


class DummyLogger:
    def __init__(self):
        self.infos = []
    def info(self, msg):
        self.infos.append(msg)


@pytest.fixture
def ctx():
    return SimpleNamespace(aws_request_id="req-123")


def _unwrap_logged_json(dummy_logger):
    assert len(dummy_logger.infos) == 1, "expected exactly one info log"
    msg = dummy_logger.infos[0]
    if isinstance(msg, (bytes, bytearray)):
        msg = msg.decode("utf-8")
    try:
        return json.loads(msg)
    except Exception:
        pytest.fail(f"logger.info did not receive JSON string: {msg!r}")


def test_log_event_with_root_id(monkeypatch, ctx):
    dummy = DummyLogger()
    monkeypatch.setattr(log_module, "logger", dummy)

    event = {
        "id": "AB_123",
        "validation": {"exists": True},
        "insert": {"inserted": False},
    }
    resp = log_module.handler(event, ctx)
    assert resp == {"logged": True}

    payload = _unwrap_logged_json(dummy)
    assert payload["level"] == "INFO"
    assert payload["msg"] == "workflow_log"
    assert payload["customer_id"] == "AB_123"
    assert payload["exists"] is True
    assert payload["inserted"] is False
    assert payload["request_id"] == "req-123"


def test_log_event_with_detail_id(monkeypatch, ctx):
    dummy = DummyLogger()
    monkeypatch.setattr(log_module, "logger", dummy)

    event = {
        "detail": {"id": "CD_456"},
        "validation": {"exists": False},
        "insert": {"inserted": True},
    }
    resp = log_module.handler(event, ctx)
    assert resp == {"logged": True}

    payload = _unwrap_logged_json(dummy)
    assert payload["customer_id"] == "CD_456"
    assert payload["exists"] is False
    assert payload["inserted"] is True
    assert payload["request_id"] == "req-123"


def test_log_event_missing_id_is_ok(monkeypatch, ctx):
    dummy = DummyLogger()
    monkeypatch.setattr(log_module, "logger", dummy)

    event = {"validation": {"exists": None}, "insert": {"inserted": None}}
    resp = log_module.handler(event, ctx)
    assert resp == {"logged": True}

    payload = _unwrap_logged_json(dummy)
    assert payload["customer_id"] is None
    assert "exists" in payload and "inserted" in payload
    assert payload["request_id"] == "req-123"


def test_log_event_handles_non_dict_event(monkeypatch, ctx):
    dummy = DummyLogger()
    monkeypatch.setattr(log_module, "logger", dummy)

    resp = log_module.handler("not-a-dict", ctx)
    assert resp == {"logged": True}

    payload = _unwrap_logged_json(dummy)
    assert payload["customer_id"] is None
    assert payload["exists"] is None
    assert payload["inserted"] is None
    assert payload["request_id"] == "req-123"


def test_lambda_handler_alias(monkeypatch, ctx):
    dummy = DummyLogger()
    monkeypatch.setattr(log_module, "logger", dummy)

    resp = log_module.lambda_handler({"id": "EF_789"}, ctx)
    assert resp == {"logged": True}
    payload = _unwrap_logged_json(dummy)
    assert payload["customer_id"] == "EF_789"
