from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from src.service.authServices import double_opt_in_user
from src.dataSource import get_db
from pydantic import BaseModel

class DoubleOptInRequest(BaseModel):
    token: str

def double_opt_in_handler(request: DoubleOptInRequest, db: Session = Depends(get_db)):
    """
    Handle user double opt-in requests.

    Args:
        request (DoubleOptInRequest): The request containing the double opt-in token.
        db (Session): The database session.

    Returns:
        dict: A success message upon successful opt-in.

    Raises:
        HTTPException: If the opt-in fails due to invalid or expired token.
    """
    try:
        user = double_opt_in_user(db, request.token)
        if user:
            return {
                "message": "Double opt-in successful.",
                "user": {
                    "id": user.id,
                    "login": user.login,
                    "role": user.role
                }
            }
        else:
            raise HTTPException(status_code=400, detail="Invalid or expired double opt-in token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
