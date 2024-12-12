from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from src.service.authServices import delete_auth_session
from src.dataSource import get_db

def delete_auth_handler(auth_id: str, db: Session = Depends(get_db)):
    """
    Handle the deletion of an authentication session by its ID.

    Args:
        auth_id (str): The ID of the authentication session to delete.
        db (Session): The database session.

    Returns:
        dict: A success message upon successful deletion.

    Raises:
        HTTPException: If the session does not exist or deletion fails.
    """
    try:
        result = delete_auth_session(db, auth_id)
        if result:
            return {"message": "Authentication session successfully deleted."}
        else:
            raise HTTPException(status_code=404, detail="Authentication session not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")