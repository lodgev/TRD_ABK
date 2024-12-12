from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from src.service.authServices import sign_up_user
from src.dataSource import get_db
from pydantic import BaseModel

class SignUpRequest(BaseModel):
    login: str
    password: str
    role: int = 0  # Default role as 0

def sign_up_handler(request: SignUpRequest, db: Session = Depends(get_db)):
    """
    Handle user sign-up requests.

    Args:
        request (SignUpRequest): The sign-up request containing user details.
        db (Session): The database session.

    Returns:
        dict: A success message upon successful sign-up.

    Raises:
        HTTPException: If sign-up fails due to an existing user or other errors.
    """
    try:
        user = sign_up_user(db, request.dict())
        return {"message": "User successfully signed up.", "user_id": user.id}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
