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

def update_bet(db: Session, bet_id: int, updates: dict):
    bet = db.query(Bet).filter(Bet.bet_id == bet_id).first()
    if not bet:
        return None

    # Dynamically update fields based on the updates dictionary
    for field, value in updates.items():
        if hasattr(bet, field):  # Ensure the Bet model has the attribute
            setattr(bet, field, value)

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
