class DomainError(Exception):
    """Base domain exception."""

    pass


class ValidationError(DomainError):
    pass


class TaskNotFoundError(DomainError):
    pass
