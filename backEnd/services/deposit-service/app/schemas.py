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
