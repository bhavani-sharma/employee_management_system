class ApplicationError(Exception):
    """Base class for errors that can be safely returned by the API."""


class EmployeeNotFoundError(ApplicationError):
    """Raised when an employee record does not exist."""


class EmployeeAlreadyExistsError(ApplicationError):
    """Raised when a unique employee email or phone number is already in use."""


class EmployeeNotEligibleError(ApplicationError):
    """Raised when an employee cannot perform the requested account action."""


class EmployeeAlreadyHasUserError(ApplicationError):
    """Raised when an employee already has a user account."""


class InvalidCredentialsError(ApplicationError):
    """Raised for invalid, expired, or revoked authentication credentials."""


class CannotDeleteOwnProfileError(ApplicationError):
    """Raised when an action would remove the caller's own access."""


class InformationValidationError(ApplicationError):
    """Raised when business-level input validation fails."""


class DuplicatePanNumberError(ApplicationError):
    """Raised when a PAN number is already assigned to an employee."""


class DatabaseOperationError(ApplicationError):
    """Raised when a database operation cannot be completed safely."""
