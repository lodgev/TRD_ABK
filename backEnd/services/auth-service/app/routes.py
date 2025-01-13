from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import User
from app.database import get_db
from app.schemas import LoginRequest, LoginResponse, LogoutRequest, LogoutResponse, RegistrationRequest, ForgotPasswordRequest, ResetPasswordRequest
from app.crud import login_user, logout_user, register_user, request_password_reset, reset_password

router = APIRouter()

@router.post("/auth/login", response_model=LoginResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    return login_user(db, data)

@router.post("/auth/logout", response_model=LogoutResponse)
def logout(data: LogoutRequest, db: Session = Depends(get_db)):
    return logout_user(db, data)

@router.post("/auth/register")
def register(data: RegistrationRequest, db: Session = Depends(get_db)):
    return register_user(db, data)
    

@router.get("/auth/verify/{user_id}")
def verify_email(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.is_verified:
        return {"message": "Email is already verified."}
    
    user.is_verified = True
    db.commit()
    return {"message": "Email successfully verified!"}

@router.post("/auth/forgot-password")
def forgot_password(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    return request_password_reset(db, data.email)

# @router.post("/auth/reset-password/{reset_token}")
# def reset_password_endpoint(data: ResetPasswordRequest, db: Session = Depends(get_db)):
#     return reset_password(db, data.reset_token, data.new_password)

@router.post("/auth/reset-password")
def reset_password_endpoint(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    return reset_password(db, data.reset_token, data.new_password)
