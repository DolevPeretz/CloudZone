from app.domain.entities import CustomerId
from app.domain.validators import is_valid_customer_id
from app.domain.errors import InvalidCustomerId
from app.ports.customer_repo import ICustomerRepository

def check_customer_exists(repo: ICustomerRepository, raw_id: str) -> bool:
    if not is_valid_customer_id(raw_id):
        raise InvalidCustomerId("invalid id format")
    return repo.exists(CustomerId(raw_id))
