from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import UserActionCreate, UserActionResponse
from app.crud import create_user_action, get_user_actions_by_user, get_user_actions_by_club
from app.database import get_db

router = APIRouter()

@router.post("/actions/", response_model=UserActionResponse)
def handle_user_action(action: UserActionCreate, db: Session = Depends(get_db)):
    try:
        return create_user_action(db, action)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing action: {str(e)}")

@router.get("/actions/user/{user_id}", response_model=list[UserActionResponse])
def get_user_actions(user_id: str, db: Session = Depends(get_db)):
    return get_user_actions_by_user(db, user_id)

@router.get("/actions/club/{club_id}", response_model=list[UserActionResponse])
def get_club_actions(club_id: int, db: Session = Depends(get_db)):
    return get_user_actions_by_club(db, club_id)
