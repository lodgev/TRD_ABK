from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from src.service.accountServices import get_account_by_id
from src.dataSource import get_db

def get_account_by_id_handler(account_id: str, db: Session = Depends(get_db)):
    """
    Handle retrieving an account by its ID.

    Args:
        account_id (str): The ID of the account to retrieve.
        db (Session): The database session.

    Returns:
        dict: The account details if found.

    Raises:
        HTTPException: If the account does not exist.
    """
    account = get_account_by_id(db, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    return {
        "id": account.id,
        "login": account.login,
        "role": account.role,
        "refresh_token": account.refresh_token,
        "registration_token": account.registration_token,
        "registrated_at": account.registrated_at,
        "last_signed_in_at": account.last_signed_in_at,
        "created_at": account.created_at,
        "updated_at": account.updated_at,
        "deleted_at": account.deleted_at,
    }
