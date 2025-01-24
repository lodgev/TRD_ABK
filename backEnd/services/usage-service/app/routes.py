import requests
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, database

router = APIRouter(prefix="/wallets", tags=["Wallets"])

# DEPOSIT_SERVICE_URL = "http://localhost:8002"
# WITHDRAWAL_SERVICE_URL = "http://localhost:8003"

DEPOSIT_SERVICE_URL = "http://deposit-service:8002/deposits"
WITHDRAWAL_SERVICE_URL = "http://withdrawal-service:8003/withdrawals"


#
@router.post("/", response_model=schemas.WalletResponse)
def create_wallet(wallet: schemas.WalletCreate, db: Session = Depends(database.get_db)):
    return crud.create_wallet(db, wallet)

@router.get("/{wallet_id}/balance", response_model=schemas.WalletBalanceResponse)
def get_balance(wallet_id: int, db: Session = Depends(database.get_db)):
    balance = crud.get_wallet_balance(db, wallet_id)
    if not balance:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return balance
#
# @router.get("/{wallet_id}/transactions", response_model=list[schemas.TransactionResponse])
# def get_transactions(wallet_id: int, db: Session = Depends(database.get_db)):
#     transactions = crud.get_wallet_transactions(db, wallet_id)
#     if not transactions:
#         raise HTTPException(status_code=404, detail="No transactions found")
#     return transactions






@router.post("/{wallet_id}/deposit")
def deposit(wallet_id: int, deposit_data: schemas.TransactionCreate, db: Session = Depends(database.get_db)):
    # Отправляем запрос в сервис депозитов
    response = requests.post(f"{DEPOSIT_SERVICE_URL}/", json={
        "wallet_id": wallet_id,
        "amount": deposit_data.amount
    })
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    # Обновляем баланс кошелька
    updated_wallet = crud.update_wallet_balance(db, wallet_id, deposit_data.amount)
    return updated_wallet

@router.post("/{wallet_id}/withdraw")
def withdraw(wallet_id: int, withdrawal_data: schemas.TransactionCreate, db: Session = Depends(database.get_db)):
    # Отправляем запрос в сервис снятия средств
    response = requests.post(f"{WITHDRAWAL_SERVICE_URL}/", json={
        "wallet_id": wallet_id,
        "amount": withdrawal_data.amount
    })
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    # Обновляем баланс кошелька
    updated_wallet = crud.update_wallet_balance(db, wallet_id, -withdrawal_data.amount)
    return updated_wallet



def make_deposit(wallet_id: int, amount: float):
    try:
        response = requests.post(
            f"{DEPOSIT_SERVICE_URL}/",
            json={"wallet_id": wallet_id, "amount": amount},
            timeout=5  # Ограничение по времени
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to deposit service: {str(e)}")

def make_withdrawal(wallet_id: int, amount: float):
    try:
        response = requests.post(
            f"{WITHDRAWAL_SERVICE_URL}/",
            json={"wallet_id": wallet_id, "amount": amount},
            timeout=5
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to withdrawal service: {str(e)}")
