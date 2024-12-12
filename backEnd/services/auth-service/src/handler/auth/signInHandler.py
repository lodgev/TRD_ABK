from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from src.service.authServices import sign_in_user
from src.dataSource import get_db
from pydantic import BaseModel

class SignInRequest(BaseModel):
    login: str
    password: str

def sign_in_handler(request: SignInRequest, db: Session = Depends(get_db)):
    """
    Handle user sign-in requests.

    Args:
        request (SignInRequest): The sign-in request containing user login and password.
        db (Session): The database session.

    Returns:
        dict: The authentication tokens and user details upon successful sign-in.

    Raises:
        HTTPException: If authentication fails.
    """
    try:
        auth_response = sign_in_user(db, request.dict())
        return {
            "message": "Sign-in successful.",
            "user": {
                "id": auth_response.user.id,
                "login": auth_response.user.login,
                "role": auth_response.user.role
            },
            "tokens": {
                "access_token": auth_response.access_token,
                "refresh_token": auth_response.refresh_token
            }
        }
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
