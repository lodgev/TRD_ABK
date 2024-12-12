class AuthServiceError(Exception):
    """
    Base class for authentication service-related errors.
    """
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

class AuthenticationFailedError(AuthServiceError):
    """
    Exception raised when user authentication fails.
    """
    def __init__(self):
        message = "Authentication failed due to invalid credentials."
        super().__init__(message)

class TokenVerificationError(AuthServiceError):
    """
    Exception raised when token verification fails.
    """
    def __init__(self, token: str):
        message = f"Token verification failed for token: {token}."
        super().__init__(message)

class UserNotFoundError(AuthServiceError):
    """
    Exception raised when a user is not found.
    """
    def __init__(self, user_id: str):
        message = f"User with ID '{user_id}' not found."
        super().__init__(message)

class AuthorizationError(AuthServiceError):
    """
    Exception raised when a user is not authorized to perform an action.
    """
    def __init__(self):
        message = "User is not authorized to perform this action."
        super().__init__(message)

class InvalidTokenError(AuthServiceError):
    """
    Exception raised when a provided token is invalid or expired.
    """
    def __init__(self):
        message = "The provided token is invalid or expired."
        super().__init__(message)
