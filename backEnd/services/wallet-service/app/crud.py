from sqlalchemy.orm import Session
from app import models, schemas
from decimal import Decimal
from fastapi import HTTPException
from app.database import get_wallet_db, get_betts_db


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
        return {"wallet_id": wallet.id, "balance": wallet.balance}
    return None


# Операции с кошельком (wallet-db)
def get_wallet(db: Session, wallet_id: int):
    return db.query(models.Wallet).filter(models.Wallet.id == wallet_id).first()

def update_wallet_balance(db: Session, wallet_id: int, amount: float):
    wallet = db.query(models.Wallet).filter(models.Wallet.id == wallet_id).first()
    if wallet:
        wallet.balance += amount
        db.commit()
        db.refresh(wallet)
    return wallet


# Функция для создания ставки с проверкой баланса
# def create_bet(db: Session, bet: schemas.BetCreate):
#     # Получаем кошелек пользователя
#     wallet = db.query(models.Wallet).filter(models.Wallet.user_id == bet.user_id).first()
#
#     if not wallet:
#         raise ValueError("Wallet not found")
#
#     # Проверяем, достаточно ли средств на балансе
#     if wallet.balance < Decimal(str(bet.amount)):
#         raise ValueError("Insufficient funds")
#
#     wallet.balance -= Decimal(str(bet.amount))
#
#
#     # Если баланс достаточен, создаем ставку и обновляем баланс
#     new_bet = models.Bet(**bet.dict())
#     db.add(new_bet)
#
#     db.commit()
#     db.refresh(new_bet)
#     db.refresh(wallet)
#
#     return new_bet


def create_bet(wallet_db: Session, bet_db: Session, bet: schemas.BetCreate):
    # Получаем кошелек пользователя из базы wallet-db
    wallet = wallet_db.query(models.Wallet).filter(models.Wallet.user_id == bet.user_id).first()

    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")

    # Проверяем, достаточно ли средств на балансе кошелька
    if wallet.balance < Decimal(str(bet.amount)):
        raise HTTPException(status_code=400, detail="Insufficient funds")

    # Списываем средства с баланса
    wallet.balance -= Decimal(str(bet.amount))
    wallet_db.commit()
    wallet_db.refresh(wallet)

    # Создаем новую ставку в базе betts-db
    new_bet = models.Bet(**bet.dict())
    bet_db.add(new_bet)
    bet_db.commit()
    bet_db.refresh(new_bet)

    return new_bet

# Операции со ставками (betts-db)
# def create_bet(db: Session, bet: schemas.BetCreate):
#     new_bet = models.Bet(
#         user_id=bet.user_id,
#         amount=bet.amount,
#         bet_type=bet.bet_type
#     )
#     db.add(new_bet)
#     db.commit()
#     db.refresh(new_bet)
#     return new_bet
