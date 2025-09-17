from infrastructure.dynamodb_repo import CustomerDynamoDBRepository
from app.domain.entities import CustomerId

repo = CustomerDynamoDBRepository()
test_id = CustomerId("user_clean_1")

print("1) exists before put:", repo.exists(test_id))  
repo.put(test_id)
print("2) exists after put:", repo.exists(test_id))   
repo.delete(test_id)
print("3) exists after delete:", repo.exists(test_id))
