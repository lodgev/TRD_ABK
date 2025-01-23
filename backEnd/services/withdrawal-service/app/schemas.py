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


# class BetCreate(BaseModel):
#     user_id: str
#     match_id: int
#     bet_type: str
#     selected_team: str
#     amount: Decimal
#     coefficient: Decimal
#     potential_win: Decimal
#
#
# class BetUpdate(BaseModel):
#     status: str = None
#     amount: float = None
#     selected_team: str = None
#     coefficient: float = None
#     potential_win: float = None
