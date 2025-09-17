from app.domain.entities import CustomerId
from app.domain.validators import is_valid_customer_id
from app.domain.errors import InvalidCustomerId
from app.ports.customer_repo import ICustomerRepository

def delete_customer_id(repo: ICustomerRepository, raw_id: str) -> None:
    if not is_valid_customer_id(raw_id):
        raise InvalidCustomerId("invalid id format")
    repo.delete(CustomerId(raw_id))
