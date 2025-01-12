from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import LoginRequest, LoginResponse, LogoutRequest, LogoutResponse, RegistrationRequest
from app.crud import login_user, logout_user, register_user_simple

router = APIRouter()

@router.post("/auth/login", response_model=LoginResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    return login_user(db, data)

@router.post("/auth/logout", response_model=LogoutResponse)
def logout(data: LogoutRequest, db: Session = Depends(get_db)):
    return logout_user(db, data)

@router.post("/auth/register")
def register(data: RegistrationRequest, db: Session = Depends(get_db)):
    return register_user_simple(db, data)
    
