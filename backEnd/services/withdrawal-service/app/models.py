


from sqlalchemy import Column, Integer, DECIMAL, String, ForeignKey, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.database import Base
#
# class Transaction(Base):
#     __tablename__ = "transactions"
#
#     id = Column(Integer, primary_key=True, index=True)
#     wallet_id = Column(Integer, nullable=False)
#     amount = Column(Float, nullable=False)
#     transaction_type = Column(String, nullable=False)
#     status = Column(String, default="pending")
#     created_at = Column(DateTime, default=func.now())
#     updated_at = Column(DateTime, default=func.now())


class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), nullable=False, unique=True, default=uuid.uuid4)
    balance = Column(DECIMAL(15, 2), nullable=False, default=0.00)
    currency = Column(String(3), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    wallet_id = Column(Integer, ForeignKey("wallets.id", ondelete="CASCADE"), nullable=False)
    amount = Column(DECIMAL(15, 2), nullable=False)
    transaction_type = Column(String(10), nullable=False)
    status = Column(String(20), nullable=False, default="pending")
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())