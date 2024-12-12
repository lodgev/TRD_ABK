from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from src.service.authServices import sign_out_user
from src.dataSource import get_db

def sign_out_handler(user_id: str, db: Session = Depends(get_db)):
    """
    Handle user sign-out requests.

    Args:
        user_id (str): The ID of the user signing out.
        db (Session): The database session.

    Returns:
        dict: A success message upon successful sign-out.

    Raises:
        HTTPException: If the sign-out process fails.
    """
    try:
        result = sign_out_user(db, user_id)
        if result:
            return {"message": "Sign-out successful."}
        else:
            raise HTTPException(status_code=404, detail="User not found or session already inactive")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
