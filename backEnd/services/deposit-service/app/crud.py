from sqlalchemy.orm import Session
from . import models, schemas


def create_transaction(db: Session, transaction: schemas.TransactionCreate):
    new_transaction = models.Transaction(
        wallet_id=transaction.wallet_id,
        amount=transaction.amount,
        transaction_type="deposit",
        status="pending"
    )
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction

# def get_transaction(db: Session, wallet_id: int):
#     return db.query(models.Transaction).filter(models.Transaction.wallet_id == wallet_id).first()
#
def get_transactions(db: Session):
    return db.query(models.Transaction).all()
