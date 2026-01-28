class DomainError(Exception):
    pass


class ValidationError(DomainError):
    pass


class TaskNotFoundError(DomainError):
    pass
