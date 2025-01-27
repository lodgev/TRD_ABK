from decimal import Decimal
from sqlalchemy.orm import Session
from app import models, schemas

def get_deposits(db: Session, wallet_id: int):
    deposits = db.query(models.Transaction).filter(
        models.Transaction.wallet_id == wallet_id,
        models.Transaction.transaction_type == "deposit"
    ).all()
    print(f"Deposits found: {deposits}")
    return deposits

def get_deposit_status(db: Session, transaction_id: int):
    transaction = db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id,
        models.Transaction.transaction_type == "deposit"
    ).first()

    if transaction:
        return {"transaction_id": transaction.id, "status": transaction.status}
    return None

def process_deposit(db: Session, deposit: schemas.TransactionCreate):
    wallet = db.query(models.Wallet).filter(models.Wallet.id == deposit.wallet_id).first()

    if not wallet:
        raise ValueError("Wallet not found")

    deposit_amount = Decimal(str(deposit.amount))

    wallet.balance += deposit_amount

    new_transaction = models.Transaction(
        wallet_id=deposit.wallet_id,
        amount=deposit_amount,
        transaction_type="deposit",
        status="completed"
    )

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    return new_transaction
