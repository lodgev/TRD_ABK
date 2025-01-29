
import logging
from uuid import UUID
from sqlalchemy.orm import Session
from app import models, schemas
from decimal import Decimal
from fastapi import HTTPException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_wallet(db: Session, wallet: schemas.WalletCreate):
    logger.info(f"Creating wallet for user_id={wallet.user_id} with currency={wallet.currency}")

    existing_wallet = db.query(models.Wallet).filter(models.Wallet.user_id == wallet.user_id).first()

    if existing_wallet:
        logger.info(f"Wallet already exists for user_id={wallet.user_id}: {existing_wallet}")
        return existing_wallet

    new_wallet = models.Wallet(
        user_id=wallet.user_id,
        balance=Decimal("0.00"),
        currency=wallet.currency
    )
    db.add(new_wallet)
    db.commit()
    db.refresh(new_wallet)

    logger.info(f"New wallet created: {new_wallet}")
    return new_wallet

def get_wallet_balance(db: Session, wallet_id: int):
    wallet = db.query(models.Wallet).filter(models.Wallet.id == wallet_id).first()
    if wallet:
        return {"wallet_id": wallet.id, "balance": wallet.balance, "currency": wallet.currency}
    return None

def get_wallet(db: Session, wallet_id: int):
    logger.info(f"Fetching wallet by wallet_id={wallet_id}")
    wallet = db.query(models.Wallet).filter(models.Wallet.id == wallet_id).first()

    if wallet:
        logger.info(f"Found wallet: {wallet}")
    else:
        logger.warning(f"No wallet found with wallet_id={wallet_id}")

    return wallet


def get_all_wallets(db: Session):
    logger.info("Fetching all wallets")
    wallets = db.query(models.Wallet).all()
    logger.info(f"Total wallets found: {len(wallets)}")
    return wallets


def get_wallet_by_user_id(db: Session, user_id: UUID, currency: str = "USD"):
    logger.info(f"Fetching wallet for user_id={user_id}")

    wallet = db.query(models.Wallet).filter(models.Wallet.user_id == str(user_id)).first()

    if not wallet:
        logger.warning(f"No wallet found for user_id={user_id}, creating a new one.")
        wallet = create_wallet(db, schemas.WalletCreate(user_id=user_id, currency=currency))

    logger.info(f"Returning wallet: {wallet}")
    return wallet


def create_bet(wallet_db: Session, bet_db: Session, bet: schemas.BetCreate):
    logger.info(f"Creating bet for user_id={bet.user_id} with amount={bet.amount}")

    wallet = wallet_db.query(models.Wallet).filter(models.Wallet.user_id == bet.user_id).first()

    if not wallet:
        logger.error(f"Wallet not found for user_id={bet.user_id}")
        raise HTTPException(status_code=404, detail="Wallet not found")

    if wallet.balance < Decimal(str(bet.amount)):
        logger.error(f"Insufficient funds for user_id={bet.user_id}: Balance={wallet.balance}, Bet={bet.amount}")
        raise HTTPException(status_code=400, detail="Insufficient funds")

    wallet.balance -= Decimal(str(bet.amount))
    wallet_db.commit()
    wallet_db.refresh(wallet)

    logger.info(f"Updated wallet balance after bet: user_id={bet.user_id}, new_balance={wallet.balance}")

    new_bet = models.Bet(**bet.dict())
    bet_db.add(new_bet)
    bet_db.commit()
    bet_db.refresh(new_bet)

    logger.info(f"Bet created: {new_bet}")
    return new_bet
