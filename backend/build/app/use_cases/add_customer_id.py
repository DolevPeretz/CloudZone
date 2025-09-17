from app.domain.entities import CustomerId
from app.domain.validators import is_valid_customer_id
from app.domain.errors import InvalidCustomerId, AlreadyExists
from app.ports.customer_repo import ICustomerRepository

def add_customer_id(repo: ICustomerRepository, raw_id: str) -> None:
    if not is_valid_customer_id(raw_id):
        raise InvalidCustomerId("invalid id format")

    cid = CustomerId(raw_id)

    if repo.exists(cid):
        raise AlreadyExists("id already exists")

    repo.put(cid)




# היא עושה שלושה דברים:
# בודקת אם ה־id חוקי (Regex).
# אם כן, בודקת אם כבר קיים ב־repo.
# אם לא קיים → מכניסה.