from pydantic import BaseModel
from datetime import datetime, date


class TransactionBase(BaseModel):
    wallet_id: int
    amount: float


class TransactionCreate(TransactionBase):
    pass


class TransactionResponse(TransactionBase):
    id: int
    transaction_type: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class TransactionStatusResponse(BaseModel):
    transaction_id: int
    status: str

    class Config:
        from_attributes = True

# id = Column(Integer, primary_key=True, index=True)
# wallet_id = Column(Integer, ForeignKey("wallets.id", ondelete="CASCADE"), nullable=False)
# amount = Column(DECIMAL(15, 2), nullable=False)
# transaction_type = Column(String(10), nullable=False)
# status = Column(String(20), nullable=False, default="pending")
# created_at = Column(TIMESTAMP, server_default=func.now())
# updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
