# # routes for the API
#

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, database

router = APIRouter(prefix="/deposit", tags=["Deposit"])

@router.post("/", response_model=schemas.TransactionResponse)
def create_deposit(deposit: schemas.TransactionCreate, db: Session = Depends(database.get_db)):
    try:
        transaction = crud.process_deposit(db, deposit)
        return transaction
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{wallet_id}", response_model=list[schemas.TransactionResponse])
def get_deposits(wallet_id: int, db: Session = Depends(database.get_db)):
    transactions = crud.get_deposits(db, wallet_id)
    if not transactions:
        raise HTTPException(status_code=404, detail="No deposits found")
    return transactions


@router.get("/status/{transaction_id}", response_model=schemas.TransactionStatusResponse)
def get_deposit_status(transaction_id: int, db: Session = Depends(database.get_db)):
    status = crud.get_deposit_status(db, transaction_id)
    if not status:
        raise HTTPException(status_code=404, detail="Deposit not found")
    return status