from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from src.service.accountServices import delete_account
from src.dataSource import get_db

def delete_account_handler(account_id: str, db: Session = Depends(get_db)):
    """
    Handle the deletion of an account by its ID.

    Args:
        account_id (str): The ID of the account to delete.
        db (Session): The database session.

    Returns:
        dict: A success message upon successful deletion.

    Raises:
        HTTPException: If the account does not exist or deletion fails.
    """
    # Attempt to delete the account
    try:
        result = delete_account(db, account_id)
        if result:
            return {"message": "Account successfully deleted."}
        else:
            raise HTTPException(status_code=404, detail="Account not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
