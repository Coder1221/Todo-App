class TodoNotFound(Exception):
    """Raised when a Todo is not found"""


class UnAuthorized(Exception):
    """Raised when a user wants to access a resource that is not authorized"""


class AlreadyOnHighestPriority(Exception):
    """Raised when a todo is already on the highest priority"""


class AlreadyOnLowPriority(Exception):
    """Raised when todo priority is already on the lowest"""
