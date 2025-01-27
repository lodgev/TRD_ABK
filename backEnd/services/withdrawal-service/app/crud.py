from sqlalchemy.orm import Session
from app import models, schemas
from decimal import Decimal


def process_withdrawal(db: Session, withdrawal: schemas.TransactionCreate):
    wallet = db.query(models.Wallet).filter(models.Wallet.id == withdrawal.wallet_id).first()

    if not wallet:
        raise ValueError("Wallet not found")

    withdrawal_amount = Decimal(str(withdrawal.amount))

    if wallet.balance < withdrawal_amount:
        raise ValueError("Insufficient funds")

    wallet.balance -= withdrawal_amount

    new_transaction = models.Transaction(
        wallet_id=withdrawal.wallet_id,
        amount=-withdrawal_amount,
        transaction_type="withdrawal",
        status="completed"
    )

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    return new_transaction



def get_withdrawals(db: Session, wallet_id: int):
    withdrawals = db.query(models.Transaction).filter(
        models.Transaction.wallet_id == wallet_id,
        models.Transaction.transaction_type == "withdrawal"
    ).all()
    print(f"Withdrawals found: {withdrawals}")
    return withdrawals


def get_withdrawal_status(db: Session, transaction_id: int):
    transaction = db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id,
        models.Transaction.transaction_type == "withdrawal"
    ).first()

    if transaction:
        return {"transaction_id": transaction.id, "status": transaction.status}
    return None