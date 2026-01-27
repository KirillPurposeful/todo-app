class DomainException(Exception):
    pass


class ValidationError(DomainException):
    pass


class TaskNotFoundError(DomainException):
    pass
