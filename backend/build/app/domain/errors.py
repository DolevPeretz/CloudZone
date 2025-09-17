class DomainError(Exception):
    pass

class InvalidCustomerId(DomainError):
    pass

class AlreadyExists(DomainError):
    pass

class NotFound(DomainError):
    pass


# errors.py
# מגדיר חריגות (Exceptions) ייחודיות ללוגיקה שלנו.
# לדוגמה:
# InvalidCustomerId — אם הפורמט לא חוקי.
# AlreadyExists — אם ה־ID כבר קיים בטבלה.
# NotFound — אם ניסינו למחוק/לבדוק משהו שלא נמצא.
# ככה מקרי השימוש יכולים "לזרוק" שגיאות ספציפיות, וה־handler ידע להחזיר תשובה מתאימה ללקוח.