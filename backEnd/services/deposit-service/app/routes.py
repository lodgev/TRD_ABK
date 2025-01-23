# # routes for the API
#

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, database

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.post("/", response_model=schemas.TransactionResponse)
def create_deposit(transaction: schemas.TransactionCreate, db: Session = Depends(database.get_db)):
    return crud.create_transaction(db, transaction)

@router.get("/", response_model=list[schemas.TransactionResponse])
def get_transactions(db: Session = Depends(database.get_db)):
    transactions = crud.get_transactions(db)
    if not transactions:
        raise HTTPException(status_code=404, detail="No transactions found")
    return transactions
