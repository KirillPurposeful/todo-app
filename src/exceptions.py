"""Domain exceptions."""


class DomainError(Exception):
    """Base exception for domain errors."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class ValidationError(DomainError):
    """Raised when domain validation fails."""
