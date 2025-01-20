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

def get_all_bets(db: Session):
    return db.query(Bet).all()

def update_bet_status(db: Session, bet_id: int, new_status: str):
    bet = db.query(Bet).filter(Bet.bet_id == bet_id).first()
    if not bet:
        return None
    bet.status = new_status
    db.commit()
    db.refresh(bet)
    return bet

def delete_bet(db: Session, bet_id: int):
    bet = db.query(Bet).filter(Bet.bet_id == bet_id).first()
    if not bet:
        return None
    db.delete(bet)
    db.commit()
    return bet_id
