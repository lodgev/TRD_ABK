from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from src.service.authServices import get_user_details
from src.dataSource import get_db
from pydantic import BaseModel

class MeRequest(BaseModel):
    token: str

def me_handler(request: MeRequest, db: Session = Depends(get_db)):
    """
    Handle retrieval of user details based on authentication token.

    Args:
        request (MeRequest): The request containing the authentication token.
        db (Session): The database session.

    Returns:
        dict: The details of the authenticated user.

    Raises:
        HTTPException: If the token is invalid or user not found.
    """
    try:
        user = get_user_details(db, request.token)
        if user:
            return {
                "id": user.id,
                "login": user.login,
                "role": user.role,
                "created_at": user.created_at,
                "updated_at": user.updated_at,
                "last_signed_in_at": user.last_signed_in_at,
            }
        else:
            raise HTTPException(status_code=401, detail="Invalid token or user not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
