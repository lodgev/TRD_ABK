from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from src.service.authServices import verify_user_token
from src.dataSource import get_db
from pydantic import BaseModel

class VerifyRequest(BaseModel):
    token: str

def verify_handler(request: VerifyRequest, db: Session = Depends(get_db)):
    """
    Handle user token verification requests.

    Args:
        request (VerifyRequest): The request containing the token to verify.
        db (Session): The database session.

    Returns:
        dict: A success message and user details if the token is valid.

    Raises:
        HTTPException: If token verification fails.
    """
    try:
        user = verify_user_token(db, request.token)
        if user:
            return {
                "message": "Token verified successfully.",
                "user": {
                    "id": user.id,
                    "login": user.login,
                    "role": user.role
                }
            }
        else:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
