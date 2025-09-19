class DomainError(Exception):
    pass

class InvalidCustomerId(DomainError):
    pass

class AlreadyExists(DomainError):
    pass

class NotFound(DomainError):
    pass