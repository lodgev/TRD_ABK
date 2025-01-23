from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, database

router = APIRouter(prefix="/withdrawals", tags=["Withdrawals"])

@router.post("/", response_model=schemas.TransactionResponse)
def create_withdrawal(withdrawal: schemas.TransactionCreate, db: Session = Depends(database.get_db)):
    try:
        return crud.create_withdrawal(db, withdrawal)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{wallet_id}", response_model=list[schemas.TransactionResponse])
def get_withdrawals(wallet_id: int, db: Session = Depends(database.get_db)):
    withdrawals = crud.get_withdrawals(db, wallet_id)
    if not withdrawals:
        raise HTTPException(status_code=404, detail="No withdrawals found")
    return withdrawals


@router.get("/status/{transaction_id}", response_model=schemas.TransactionStatusResponse)
def get_withdrawal_status(transaction_id: int, db: Session = Depends(database.get_db)):
    status = crud.get_withdrawal_status(db, transaction_id)
    if not status:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return status