import re
from app.errors import InvalidCustomerId

_ID_RE = re.compile(r"^[A-Za-z0-9_-]{3,64}$")

def is_valid_customer_id(s: str | None) -> bool:
    return bool(s) and isinstance(s, str) and bool(_ID_RE.match(s))

def validate_id(cid: str | None) -> str:
    if not is_valid_customer_id(cid):
        raise InvalidCustomerId(f"Invalid or missing 'id': {cid}")
    return cid
