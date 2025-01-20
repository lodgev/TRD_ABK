from sqlalchemy.orm import Session
from app.models import Bet
from app.schemas import BetCreate

def create_bet(db: Session, bet: BetCreate):
    new_bet = Bet(**bet.dict())
    db.add(new_bet)
    db.commit()
    db.refresh(new_bet)
    return new_bet

def get_bet(db: Session, bet_id: int):
    return db.query(Bet).filter(Bet.bet_id == bet_id).first()
