
from sqlalchemy import Column, Integer, DECIMAL, String, ForeignKey, TIMESTAMP, func, Enum
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.database import WalletBase, BettsBase

class Wallet(WalletBase):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), nullable=False, unique=True, default=uuid.uuid4)
    balance = Column(DECIMAL(15, 2), nullable=False, default=0.00)
    currency = Column(String(3), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

class Transaction(WalletBase):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    wallet_id = Column(Integer, ForeignKey("wallets.id", ondelete="CASCADE"), nullable=False)
    amount = Column(DECIMAL(15, 2), nullable=False)
    transaction_type = Column(String(10), nullable=False)
    status = Column(String(20), nullable=False, default="pending")
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

# ................................................
class Bet(BettsBase):
    __tablename__ = "bets"

    bet_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    match_id = Column(Integer, nullable=False)
    bet_type = Column(Enum("win", "lose", "draw", name="bet_type_enum"), nullable=False)
    selected_team = Column(String(255), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    potential_win = Column(DECIMAL(10, 2), nullable=False)
    coefficient = Column(DECIMAL(5, 2), nullable=False)
    status = Column(Enum("waiting_list", "pending", "won", "lost", name="status_enum"), default="waiting_list")
    created_at = Column(TIMESTAMP, nullable=False)
