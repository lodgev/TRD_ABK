from sqlalchemy.orm import Session
from app import models, schemas
from decimal import Decimal

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

