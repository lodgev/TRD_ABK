from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import LoginRequest, LoginResponse
from app.crud import login_user, logout_user

router = APIRouter()

@router.post("/auth/login", response_model=LoginResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    return login_user(db, data)

# @router.post("/auth/logout")
# def logout(user_id: str, db: Session = Depends(get_db)):
#     return logout_user(db, user_id)