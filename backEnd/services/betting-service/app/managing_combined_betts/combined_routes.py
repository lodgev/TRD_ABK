# combined_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.managing_combined_betts.combined_crud import create_combined_bet
from app.schemas import CombinedBetCreate, CombinedBetResponse

router = APIRouter()

@router.post("/create-combined-bet", response_model=CombinedBetResponse)
def create_combined_bet_endpoint(
    bet_data: CombinedBetCreate,
    db: Session = Depends(get_db)
):
    try:
        combined_bet = create_combined_bet(db, bet_data)
        return combined_bet
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
