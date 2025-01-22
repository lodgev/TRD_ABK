from fastapi import APIRouter, HTTPException, Depends
from app.managing_betts import crud

from app.schemas import BetCreate, BetUpdate
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter()

@router.post("/create-bet")
def create_bet(bet: BetCreate, db: Session = Depends(get_db)):
    print("Received JSON:", bet.dict())
    return crud.create_bet(db, bet)

@router.get("/get-bet/{bet_id}")
def get_bet(bet_id: int, db: Session = Depends(get_db)):
    bet = crud.get_bet(db, bet_id)
    if not bet:
        raise HTTPException(status_code=404, detail="Bet not found")
    return bet

@router.get("/get-all-bets")
def get_all_bets(db: Session = Depends(get_db)):
    bets = crud.get_all_bets(db)
    if not bets:
        raise HTTPException(status_code=404, detail="No bets found")
    return bets

# @router.put("/update-bet/{bet_id}", response_model=dict)
# def update_bet(bet_id: int, bet_update: BetUpdate, db: Session = Depends(get_db)):
#     bet = crud.update_bet_status(db, bet_id, bet_update.status)
#     if not bet:
#         raise HTTPException(status_code=404, detail="Bet not found")
#     return {"message": "Bet updated successfully", "bet_id": bet_id, "new_status": bet.status}

@router.put("/update-bet/{bet_id}", response_model=dict)
def update_bet(bet_id: int, bet_update: BetUpdate, db: Session = Depends(get_db)):
    updates = bet_update.dict(exclude_unset=True)  # Extract only provided fields
    bet = crud.update_bet(db, bet_id, updates)
    if not bet:
        raise HTTPException(status_code=404, detail="Bet not found")
    return {
        "message": "Bet updated successfully",
        "bet_id": bet_id,
        "updated_fields": updates,
    }

@router.delete("/cancel-bet/{bet_id}", response_model=dict)
def cancel_bet(bet_id: int, db: Session = Depends(get_db)):
    bet_id_deleted = crud.delete_bet(db, bet_id)
    if not bet_id_deleted:
        raise HTTPException(status_code=404, detail="Bet not found")
    return {"message": "Bet canceled successfully", "bet_id": bet_id}
