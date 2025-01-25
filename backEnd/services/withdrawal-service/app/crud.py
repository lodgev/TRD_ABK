from sqlalchemy.orm import Session
from app import models, schemas
from decimal import Decimal


def create_withdrawal(db: Session, withdrawal: schemas.TransactionCreate):
    # Проверка наличия средств на кошельке
    wallet_balance = db.query(models.Transaction).filter(
        models.Transaction.wallet_id == withdrawal.wallet_id
    ).with_entities(models.Transaction.amount).all()

    total_balance = sum(t.amount for t in wallet_balance)

    if total_balance < withdrawal.amount:
        raise ValueError("Insufficient funds")

    new_transaction = models.Transaction(
        wallet_id=withdrawal.wallet_id,
        amount=-withdrawal.amount,  # Сумма отрицательная для вывода
        transaction_type="withdrawal",
        status="pending"
    )
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction



def process_withdrawal(db: Session, withdrawal: schemas.TransactionCreate):
    # Получаем баланс кошелька
    wallet = db.query(models.Wallet).filter(models.Wallet.id == withdrawal.wallet_id).first()

    if not wallet:
        raise ValueError("Wallet not found")

    # Преобразование суммы к Decimal для корректной арифметики
    withdrawal_amount = Decimal(str(withdrawal.amount))

    # Проверяем наличие средств на счете
    if wallet.balance < withdrawal_amount:
        raise ValueError("Insufficient funds")

    # Обновляем баланс кошелька
    wallet.balance -= withdrawal_amount

    # Создаем запись транзакции
    new_transaction = models.Transaction(
        wallet_id=withdrawal.wallet_id,
        amount=-withdrawal_amount,  # Отрицательное значение для снятия
        transaction_type="withdrawal",
        status="completed"  # Устанавливаем статус как "завершено"
    )

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    return new_transaction


# def get_withdrawals(db: Session, wallet_id: int):
#     return db.query(models.Transaction).filter(
#         models.Transaction.wallet_id == wallet_id,
#         models.Transaction.transaction_type == "withdrawal"
#     ).all()

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