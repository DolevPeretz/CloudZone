from abc import ABC, abstractmethod
from app.domain.entities import CustomerId

class ICustomerRepository(ABC):
    @abstractmethod
    def put(self, cid: CustomerId) -> None:
        ...

    @abstractmethod
    def exists(self, cid: CustomerId) -> bool:
        ...

    @abstractmethod
    def delete(self, cid: CustomerId) -> None:
        ...


# put → להכניס CustomerId
# exists → לבדוק אם קיים
# delete → למחוק