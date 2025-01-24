from sqlalchemy.orm import Session
from app import models, schemas
from decimal import Decimal

def create_wallet(db: Session, wallet: schemas.WalletCreate):
    new_wallet = models.Wallet(
        user_id=wallet.user_id,
        balance=Decimal("0.00"),
        currency=wallet.currency
    )
    db.add(new_wallet)
    db.commit()
    db.refresh(new_wallet)
    return new_wallet


def update_wallet_balance(db: Session, wallet_id: int, amount: Decimal):
    wallet = db.query(models.Wallet).filter(models.Wallet.id == wallet_id).first()

    if not wallet:
        raise ValueError("Wallet not found")

    wallet.balance += Decimal(amount)
    db.commit()
    db.refresh(wallet)
    return wallet

def get_wallet_balance(db: Session, wallet_id: int):
    wallet = db.query(models.Wallet).filter(models.Wallet.id == wallet_id).first()
    if wallet:
        return {"wallet_id": wallet.id, "balance": wallet.balance}
    return None

# def get_wallet_transactions(db: Session, wallet_id: int):
#     return db.query(models.Transaction).filter(models.Transaction.wallet_id == wallet_id).all()

# def create_transaction(db: Session, transaction: schemas.TransactionCreate):
#     usage = db.query(models.Wallet).filter(models.Wallet.id == transaction.wallet_id).first()
#
#     if not usage:
#         raise HTTPException(status_code=404, detail="Wallet not found")
#
#     # Проверка доступного баланса для вывода средств
#     if transaction.transaction_type == "withdrawal" and usage.balance < transaction.amount:
#         raise HTTPException(status_code=400, detail="Insufficient funds")
#
#     # Создание транзакции
#     new_transaction = models.Transaction(
#         wallet_id=transaction.wallet_id,
#         amount=transaction.amount,
#         transaction_type=transaction.transaction_type,
#         status="completed"
#     )
#
#     # Обновление баланса
#     if transaction.transaction_type == "deposit":
#         usage.balance += Decimal(transaction.amount)
#     elif transaction.transaction_type == "withdrawal":
#         usage.balance -= Decimal(transaction.amount)
#
#     db.add(new_transaction)
#     db.commit()
#     db.refresh(usage)
#     db.refresh(new_transaction)
#     return new_transaction