from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.dataSource import get_db
from src.handler.account.createAccountHandler import create_account_handler
from src.handler.account.getAccountByIdHandler import get_account_by_id_handler
from src.handler.account.getAllAccountsHandler import get_all_accounts_handler
from src.handler.account.deleteAccountHandler import delete_account_handler
from pydantic import BaseModel

router = APIRouter()

class CreateAccountRequest(BaseModel):
    login: str
    password: str
    role: int = 0

@router.post("/accounts")
def create_account(request: CreateAccountRequest, db: Session = Depends(get_db)):
    """
    Endpoint to create a new account.

    Args:
        request (CreateAccountRequest): The account details.
        db (Session): The database session.

    Returns:
        dict: A success message and the created account's ID.
    """
    return create_account_handler(request, db)

@router.get("/accounts/{account_id}")
def get_account_by_id(account_id: str, db: Session = Depends(get_db)):
    """
    Endpoint to retrieve an account by ID.

    Args:
        account_id (str): The ID of the account to retrieve.
        db (Session): The database session.

    Returns:
        dict: The account details.
    """
    return get_account_by_id_handler(account_id, db)

@router.get("/accounts")
def get_all_accounts(db: Session = Depends(get_db)):
    """
    Endpoint to retrieve all accounts.

    Args:
        db (Session): The database session.

    Returns:
        list: A list of all accounts.
    """
    return get_all_accounts_handler(db)

@router.delete("/accounts/{account_id}")
def delete_account(account_id: str, db: Session = Depends(get_db)):
    """
    Endpoint to delete an account by ID.

    Args:
        account_id (str): The ID of the account to delete.
        db (Session): The database session.

    Returns:
        dict: A success message upon successful deletion.
    """
    return delete_account_handler(account_id, db)
