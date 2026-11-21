class ServiceDeskError(Exception):
    """Base exception for expected service-desk errors."""


class DuplicateRequestIdError(ServiceDeskError):
    """Raised when a request ID is already in use."""


class RequestNotFoundError(ServiceDeskError):
    """Raised when a request ID cannot be found."""


class InvalidPriorityError(ServiceDeskError):
    """Raised when a priority is not LOW, MEDIUM, or HIGH."""


class RequestAlreadyResolvedError(ServiceDeskError):
    """Raised when a resolved request is resolved again."""


class InvalidMenuChoiceError(ServiceDeskError):
    """Raised when a menu choice is not one of the available options."""
