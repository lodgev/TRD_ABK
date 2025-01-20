from fastapi import APIRouter, HTTPException, Depends
from app.managing_betts import crud

from app.schemas import BetCreate
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter()

@router.post("/create-bet")
def create_bet(bet: BetCreate, db: Session = Depends(get_db)):
    return crud.create_bet(db, bet)

@router.get("/get-bet/{bet_id}")
def get_bet(bet_id: int, db: Session = Depends(get_db)):
    bet = crud.get_bet(db, bet_id)
    if not bet:
        raise HTTPException(status_code=404, detail="Bet not found")
    return bet
