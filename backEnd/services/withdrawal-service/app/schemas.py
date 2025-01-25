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



# class WalletBase(BaseModel):
#     user_id: int
#     balance: float
#     currency: str
#
# class WalletResponse(WalletBase):
#     id: int
#     created_at: datetime
#
#     class Config:
#         orm_mode = True