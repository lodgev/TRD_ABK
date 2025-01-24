from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_wallet_db, get_betts_db
from app import crud, schemas

router = APIRouter(prefix="/wallets", tags=["Wallets"])

#
@router.post("/", response_model=schemas.WalletResponse)
def create_wallet(wallet: schemas.WalletCreate, db: Session = Depends(get_wallet_db)):
    return crud.create_wallet(db, wallet)

@router.get("/{wallet_id}/balance", response_model=schemas.WalletBalanceResponse)
def get_balance(wallet_id: int, db: Session = Depends(get_wallet_db)):
    balance = crud.get_wallet_balance(db, wallet_id)
    if not balance:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return balance


# Работа с кошельком
@router.get("/wallet/{wallet_id}", response_model=schemas.WalletResponse)
def read_wallet(wallet_id: int, db: Session = Depends(get_wallet_db)):
    wallet = crud.get_wallet(db, wallet_id)
    if wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet
#
# @router.post("/wallet/deposit/")
# def deposit_funds(wallet: schemas.WalletDeposit, db: Session = Depends(get_wallet_db)):
#     updated_wallet = crud.update_wallet_balance(db, wallet.wallet_id, wallet.amount)
#     if not updated_wallet:
#         raise HTTPException(status_code=404, detail="Wallet not found")
#     return {"message": "Deposit successful", "balance": updated_wallet.balance}

# Работа со ставками
@router.post("/bets/", response_model=schemas.BetResponse)
def place_bet(bet: schemas.BetCreate, db: Session = Depends(get_betts_db)):
    new_bet = crud.create_bet(db, bet)
    return new_bet

