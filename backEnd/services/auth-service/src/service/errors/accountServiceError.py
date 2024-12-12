class AccountServiceError(Exception):
    """
    Base class for account service-related errors.
    """
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

class AccountNotFoundError(AccountServiceError):
    """
    Exception raised when an account is not found.
    """
    def __init__(self, account_id: str):
        message = f"Account with ID '{account_id}' not found."
        super().__init__(message)

class DuplicateAccountError(AccountServiceError):
    """
    Exception raised when an account with the same login already exists.
    """
    def __init__(self, login: str):
        message = f"An account with login '{login}' already exists."
        super().__init__(message)

class AccountDeletionError(AccountServiceError):
    """
    Exception raised when an account cannot be deleted.
    """
    def __init__(self, account_id: str):
        message = f"Failed to delete account with ID '{account_id}'."
        super().__init__(message)

class InvalidAccountDataError(AccountServiceError):
    """
    Exception raised when provided account data is invalid.
    """
    def __init__(self, message: str):
        super().__init__(message)
