# define user-defined exceptions
class Error(Exception):
    """Base class for other exceptions"""
    pass


class RecipeNotFound(Error):
    """Raised when the input value is too small"""
    pass


class RecipeBeingUsed(Error):
    """Raised when the input value is too large"""
    pass