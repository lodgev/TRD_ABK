from decimal import Decimal
from sqlalchemy.orm import Session
from app import models, schemas

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




def process_deposit(db: Session, deposit: schemas.TransactionCreate):
    # Получаем кошелек
    wallet = db.query(models.Wallet).filter(models.Wallet.id == deposit.wallet_id).first()

    if not wallet:
        raise ValueError("Wallet not found")

    # Преобразование суммы депозита к Decimal для точных вычислений
    deposit_amount = Decimal(str(deposit.amount))

    # Обновляем баланс кошелька
    wallet.balance += deposit_amount

    # Создаем запись транзакции
    new_transaction = models.Transaction(
        wallet_id=deposit.wallet_id,
        amount=deposit_amount,
        transaction_type="deposit",
        status="completed"  # Устанавливаем статус как "завершено"
    )

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    return new_transaction
