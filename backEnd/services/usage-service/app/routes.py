

import uuid
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_wallet_db, get_betts_db
from app import crud, schemas

router = APIRouter(prefix="/wallet", tags=["Wallet"])

# Получить список всех кошельков
@router.get("/all-wallets")
def all_wallets(db: Session = Depends(get_wallet_db)):
    wallets = crud.get_all_wallets(db)
    if not wallets:
        raise HTTPException(status_code=404, detail="No wallets found")
    return wallets

# Получить кошелек по ID пользователя
@router.get("/user/{user_id}")
def get_wallet_id(user_id: uuid.UUID, db: Session = Depends(get_wallet_db)):
    try:
        wallet = crud.get_wallet_by_user_id(db, str(user_id))
        return wallet
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# Получить баланс кошелька по ID
@router.get("/{wallet_id}/balance", response_model=schemas.WalletBalanceResponse)
def get_balance(wallet_id: int, db: Session = Depends(get_wallet_db)):
    balance = crud.get_wallet_balance(db, wallet_id)
    if balance is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return balance

# Получить информацию о кошельке по ID
@router.get("/{wallet_id}", response_model=schemas.WalletResponse)
def read_wallet(wallet_id: int, db: Session = Depends(get_wallet_db)):
    wallet = crud.get_wallet(db, wallet_id)
    if wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet

# Создать новый кошелек
@router.post("/", response_model=schemas.WalletResponse)
def create_wallet(wallet: schemas.WalletCreate, db: Session = Depends(get_wallet_db)):
    return crud.create_wallet(db, wallet)

# Создать ставку и обновить баланс кошелька
@router.post("/create-bet", response_model=schemas.BetCreate)
def place_bet(bet: schemas.BetCreate, wallet_db: Session = Depends(get_wallet_db), bet_db: Session = Depends(get_betts_db)):
    return crud.create_bet(wallet_db, bet_db, bet)


@router.put("/{wallet_id}/update-balance")
def update_balance(wallet_id: int, request: schemas.WalletUpdate, db: Session = Depends(get_wallet_db)):
    wallet = crud.get_wallet(db, wallet_id)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")

    try:
        amount = Decimal(str(request.amount))  # Преобразование в Decimal
        if wallet.balance + amount < Decimal("0"):
            raise HTTPException(status_code=400, detail="Insufficient funds")

        wallet.balance += amount  # Корректное обновление баланса
        db.commit()
        db.refresh(wallet)
        return {"id": wallet.id, "balance": wallet.balance, "currency": wallet.currency}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating balance: {str(e)}")