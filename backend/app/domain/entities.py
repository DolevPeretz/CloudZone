from dataclasses import dataclass

@dataclass(frozen=True)
class CustomerId:
    value: str


# entities.py
# מגדיר ישות דומיין. במקרה שלנו CustomerId, אובייקט עם שדה אחד (value).
# השימוש ב־@dataclass(frozen=True) הופך אותו ל־immutable (כמו ערך טהור שלא