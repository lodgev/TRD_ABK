from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_wallet_db, get_betts_db
from app import crud, schemas

router = APIRouter(prefix="/wallet", tags=["Wallet"])

#
@router.post("/", response_model=schemas.WalletResponse)
def create_wallet(wallet: schemas.WalletCreate, db: Session = Depends(get_wallet_db)):
    return crud.create_wallet(db, wallet)

@router.get("/{wallet_id}/balance", response_model=schemas.WalletBalanceResponse)
def get_balance(wallet_id: int, db: Session = Depends(get_wallet_db)):
    balance = crud.get_wallet_balance(db, wallet_id)
    if not balance:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return balance


@router.get("/{wallet_id}", response_model=schemas.WalletResponse)
def read_wallet(wallet_id: int, db: Session = Depends(get_wallet_db)):
    wallet = crud.get_wallet(db, wallet_id)
    if wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet


@router.get("/", response_model=schemas.WalletResponse)
def all_wallets(db: Session = Depends(get_wallet_db)):
    wallet = crud.get_all_wallets(db)
    if wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet



@router.post("/create-bet", response_model=schemas.BetCreate)
def place_bet(bet: schemas.BetCreate, wallet_db: Session = Depends(get_wallet_db), bet_db: Session = Depends(get_betts_db)):
    return crud.create_bet(wallet_db, bet_db, bet)


@router.get("/wallets/user/{user_id}")
def get_wallet_id(user_id: UUID, db: Session = Depends(get_wallet_db)):
    try:
        wallet_id = crud.get_wallet_id_by_user_id(db, user_id)
        return wallet_id
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))