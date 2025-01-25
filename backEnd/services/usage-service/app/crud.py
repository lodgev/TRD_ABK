from sqlalchemy.orm import Session
from app import models, schemas
from decimal import Decimal
from fastapi import HTTPException


def create_wallet(db: Session, wallet: schemas.WalletCreate):
    existing_wallet = db.query(models.Wallet).filter(models.Wallet.user_id == wallet.user_id).first()

    if existing_wallet:
        raise ValueError("Wallet for this user already exists")

    new_wallet = models.Wallet(
        user_id=wallet.user_id,
        balance=Decimal("0.00"),
        currency=wallet.currency
    )
    db.add(new_wallet)
    db.commit()
    db.refresh(new_wallet)
    return new_wallet


def get_wallet_balance(db: Session, wallet_id: int):
    wallet = db.query(models.Wallet).filter(models.Wallet.id == wallet_id).first()
    if wallet:
        return {"wallet_id": wallet.id, "balance": wallet.balance, "currency": wallet.currency}
    return None


def get_wallet(db: Session, wallet_id: int):
    return db.query(models.Wallet).filter(models.Wallet.id == wallet_id).first()


def create_bet(wallet_db: Session, bet_db: Session, bet: schemas.BetCreate):
    wallet = wallet_db.query(models.Wallet).filter(models.Wallet.user_id == bet.user_id).first()

    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")

    if wallet.balance < Decimal(str(bet.amount)):
        raise HTTPException(status_code=400, detail="Insufficient funds")

    wallet.balance -= Decimal(str(bet.amount))
    wallet_db.commit()
    wallet_db.refresh(wallet)

    new_bet = models.Bet(**bet.dict())
    bet_db.add(new_bet)
    bet_db.commit()
    bet_db.refresh(new_bet)

    return new_bet

