class TodoNotFound(Exception):
    """Raised when a Todo is not found"""


class TodoCreationError(Exception):
    """Raised when a Todo is not created"""


class UnAuthorized(Exception):
    """Raised when a user wants to access a resource that is not authorized"""


class AlreadyOnHighestPriority(Exception):
    """Raised when a todo is already on the highest priority"""


class AlreadyOnLowPriority(Exception):
    """Raised when todo priority is already on the lowest"""


class LoginFailure(Exception):
    """Raised when user password is incorrect"""


class RecordNotUpdated(Exception):
    """Raised when a record is not updated in repository"""


class InvalidJwtToken(Exception):
    """Raised when given token is invalid"""


class UserNotFound(Exception):
    """Raised when a user is not found given email"""


class TodoAttributeMissingError(Exception):
    """Raised when a todo attribute is missing in request"""
