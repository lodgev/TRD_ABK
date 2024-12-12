from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from src.service.accountServices import get_all_accounts
from src.dataSource import get_db

def get_all_accounts_handler(db: Session = Depends(get_db)):
    """
    Handle retrieving all accounts.

    Args:
        db (Session): The database session.

    Returns:
        list: A list of all account details.

    Raises:
        HTTPException: If an error occurs while fetching accounts.
    """
    try:
        accounts = get_all_accounts(db)
        return [
            {
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
            for account in accounts
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
