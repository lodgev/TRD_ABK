from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.dataSource import get_db
from src.handler.auth.signUpHandler import sign_up_handler
from src.handler.auth.signInHandler import sign_in_handler
from src.handler.auth.signOutHandler import sign_out_handler
from src.handler.auth.verifyHandler import verify_handler
from src.handler.auth.doubleOptinHandler import double_opt_in_handler
from src.handler.auth.meHandler import me_handler
from pydantic import BaseModel

router = APIRouter()

class SignUpRequest(BaseModel):
    login: str
    password: str
    role: int = 0

class SignInRequest(BaseModel):
    login: str
    password: str

class VerifyRequest(BaseModel):
    token: str

class DoubleOptInRequest(BaseModel):
    token: str

class MeRequest(BaseModel):
    token: str

@router.post("/auth/signup")
def sign_up(request: SignUpRequest, db: Session = Depends(get_db)):
    """
    Endpoint to sign up a new user.

    Args:
        request (SignUpRequest): The sign-up request containing user details.
        db (Session): The database session.

    Returns:
        dict: A success message and the user's ID upon successful sign-up.
    """
    return sign_up_handler(request, db)

@router.post("/auth/signin")
def sign_in(request: SignInRequest, db: Session = Depends(get_db)):
    """
    Endpoint to sign in a user.

    Args:
        request (SignInRequest): The sign-in request containing user credentials.
        db (Session): The database session.

    Returns:
        dict: The authentication tokens and user details upon successful sign-in.
    """
    return sign_in_handler(request, db)

@router.post("/auth/signout")
def sign_out(user_id: str, db: Session = Depends(get_db)):
    """
    Endpoint to sign out a user.

    Args:
        user_id (str): The ID of the user signing out.
        db (Session): The database session.

    Returns:
        dict: A success message upon successful sign-out.
    """
    return sign_out_handler(user_id, db)

@router.post("/auth/verify")
def verify(request: VerifyRequest, db: Session = Depends(get_db)):
    """
    Endpoint to verify a user's authentication token.

    Args:
        request (VerifyRequest): The request containing the token to verify.
        db (Session): The database session.

    Returns:
        dict: A success message and user details if the token is valid.
    """
    return verify_handler(request, db)

@router.post("/auth/double-optin")
def double_opt_in(request: DoubleOptInRequest, db: Session = Depends(get_db)):
    """
    Endpoint to handle user double opt-in.

    Args:
        request (DoubleOptInRequest): The request containing the double opt-in token.
        db (Session): The database session.

    Returns:
        dict: A success message upon successful double opt-in.
    """
    return double_opt_in_handler(request, db)

@router.get("/auth/me")
def me(request: MeRequest, db: Session = Depends(get_db)):
    """
    Endpoint to retrieve authenticated user details.

    Args:
        request (MeRequest): The request containing the authentication token.
        db (Session): The database session.

    Returns:
        dict: The details of the authenticated user.
    """
    return me_handler(request, db)
