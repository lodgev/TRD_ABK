from sqlalchemy.orm import Session
from app.models import UserAction
from app.schemas import UserActionCreate

def create_user_action(db: Session, action_data: UserActionCreate):
    new_action = UserAction(**action_data.dict())
    db.add(new_action)
    db.commit()
    db.refresh(new_action)
    return new_action

def get_user_actions_by_user(db: Session, user_id: str):
    return db.query(UserAction).filter(UserAction.user_id == user_id).all()

def get_user_actions_by_club(db: Session, club_id: int):
    return db.query(UserAction).filter(UserAction.club_id == club_id).all()
