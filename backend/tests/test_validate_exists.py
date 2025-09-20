import pytest
from lambdas.validate_exists import handler as ve_module

# ----- Dummy repos -----
class RepoExistsTrue:
    def exists(self, _id): return True

class RepoExistsFalse:
    def exists(self, _id): return False

class RepoCrash:
    def exists(self, _id): raise RuntimeError("db error")

# ----- Stub validators -----
def _stub_validate_identity(x): return x
def _stub_validate_raises(_): raise ValueError("invalid id")

# ----- Event fixtures -----
@pytest.fixture
def ev_root():
    return {"id": "AB_123"}

@pytest.fixture
def ev_detail():
    return {"detail": {"id": "AB_123"}}

@pytest.fixture
def ev_path():
    return {"pathParameters": {"id": "AB_123"}, "headers": {}}

@pytest.fixture
def ev_header():
    return {"headers": {"ID": "AB_123"}, "pathParameters": None}

@pytest.fixture
def ev_not_dict():
    return "not-a-dict"

# ----- Tests -----
def test_exists_true_from_root(monkeypatch, ev_root):
    monkeypatch.setattr(ve_module, "validate_id", _stub_validate_identity)
    monkeypatch.setattr(ve_module, "repo", RepoExistsTrue())

    resp = ve_module.handler(ev_root, context=None)
    assert resp == {"exists": True}

def test_exists_false_from_detail(monkeypatch, ev_detail):
    monkeypatch.setattr(ve_module, "validate_id", _stub_validate_identity)
    monkeypatch.setattr(ve_module, "repo", RepoExistsFalse())

    resp = ve_module.handler(ev_detail, context=None)
    assert resp == {"exists": False}

def test_exists_true_from_path(monkeypatch, ev_path):
    monkeypatch.setattr(ve_module, "validate_id", _stub_validate_identity)
    monkeypatch.setattr(ve_module, "repo", RepoExistsTrue())

    resp = ve_module.handler(ev_path, context=None)
    assert resp == {"exists": True}

def test_exists_true_from_header(monkeypatch, ev_header):
    monkeypatch.setattr(ve_module, "validate_id", _stub_validate_identity)
    monkeypatch.setattr(ve_module, "repo", RepoExistsTrue())

    resp = ve_module.handler(ev_header, context=None)
    assert resp == {"exists": True}

def test_invalid_id_raises(monkeypatch, ev_root):
    monkeypatch.setattr(ve_module, "validate_id", _stub_validate_raises)
    monkeypatch.setattr(ve_module, "repo", RepoExistsTrue())

    with pytest.raises(Exception):
        ve_module.handler(ev_root, context=None)

def test_event_not_dict_invalid_raises(monkeypatch, ev_not_dict):
    # _extract_id יחזיר None → validate_id יזרוק
    monkeypatch.setattr(ve_module, "validate_id", _stub_validate_raises)
    monkeypatch.setattr(ve_module, "repo", RepoExistsTrue())

    with pytest.raises(Exception):
        ve_module.handler(ev_not_dict, context=None)

def test_repo_crash_raises(monkeypatch, ev_root):
    monkeypatch.setattr(ve_module, "validate_id", _stub_validate_identity)
    monkeypatch.setattr(ve_module, "repo", RepoCrash())

    with pytest.raises(Exception):
        ve_module.handler(ev_root, context=None)
