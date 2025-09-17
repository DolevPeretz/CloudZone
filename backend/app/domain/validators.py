import re

_ID_RE = re.compile(r"^[A-Za-z0-9_-]{3,64}$")

def is_valid_customer_id(s: str) -> bool:
    return bool(s) and bool(_ID_RE.match(s))


# מכיל פונקציות ולידציה. כאן יש Regex שבודק האם מזהה הלקוח (id) עומד בחוקים (3–64 תווים, אותיות/מספרים/_/-).
# הפונקציה is_valid_customer_id("user_123") → True.