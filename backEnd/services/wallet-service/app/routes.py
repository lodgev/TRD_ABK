from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, database

router = APIRouter(prefix="/wallets", tags=["Wallets"])

@router.post("/", response_model=schemas.WalletResponse)
def create_wallet(wallet: schemas.WalletCreate, db: Session = Depends(database.get_db)):
    return crud.create_wallet(db, wallet)

@router.get("/{wallet_id}/balance", response_model=schemas.WalletBalanceResponse)
def get_balance(wallet_id: int, db: Session = Depends(database.get_db)):
    balance = crud.get_wallet_balance(db, wallet_id)
    if not balance:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return balance

@router.get("/{wallet_id}/transactions", response_model=list[schemas.TransactionResponse])
def get_transactions(wallet_id: int, db: Session = Depends(database.get_db)):
    transactions = crud.get_wallet_transactions(db, wallet_id)
    if not transactions:
        raise HTTPException(status_code=404, detail="No transactions found")
    return transactions
