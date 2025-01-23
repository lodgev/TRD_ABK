from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class WalletBase(BaseModel):
    user_id: UUID
    currency: str

class WalletCreate(WalletBase):
    pass

class WalletResponse(WalletBase):
    id: int
    balance: float
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class WalletBalanceResponse(BaseModel):
    wallet_id: int
    balance: float

class TransactionResponse(BaseModel):
    id: int
    wallet_id: int
    amount: float
    transaction_type: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
