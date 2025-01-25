# # routes for the API
#

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, database

router = APIRouter(prefix="/deposits", tags=["Deposits"])

# @router.post("/", response_model=schemas.TransactionResponse)
# def create_deposit(deposit: schemas.TransactionCreate, db: Session = Depends(database.get_db)):
#     deposit_transaction = crud.create_transaction(db, deposit)
#     if not deposit_transaction:
#         raise HTTPException(status_code=400, detail="Deposit failed")
#     return deposit_transaction

@router.post("/", response_model=schemas.TransactionResponse)
def create_deposit(deposit: schemas.TransactionCreate, db: Session = Depends(database.get_db)):
    try:
        transaction = crud.process_deposit(db, deposit)
        return transaction
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[schemas.TransactionResponse])
def get_transactions(db: Session = Depends(database.get_db)):
    transactions = crud.get_transactions(db)
    if not transactions:
        raise HTTPException(status_code=404, detail="No transactions found")
    return transactions


