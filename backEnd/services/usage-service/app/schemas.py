from decimal import Decimal

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
    user_id: int
    balance: float
    currency: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class WalletBalanceResponse(BaseModel):
    wallet_id: int
    balance: float
    # currency: str
#
# class TransactionResponse(BaseModel):
#     id: int
#     wallet_id: int
#     amount: float
#     transaction_type: str
#     status: str
#     created_at: datetime
#     updated_at: datetime
#
#     class Config:
#         from_attributes = True
#
#
# class TransactionCreate(BaseModel):
#     wallet_id: int
#     amount: float


# ......................

class BetCreate(BaseModel):
    user_id: str
    match_id: int
    bet_type: str
    selected_team: str
    amount: Decimal
    coefficient: Decimal
    potential_win: Decimal

# Схемы для ставок (betts-db)
# class BetCreate(BaseModel):
#     user_id: int
#     amount: float
#     bet_type: str

class BetResponse(BetCreate):
    id: int
    # amount: float
    # bet_type: str
    # selected_team: str
    created_at: datetime

    class Config:
        from_attributes = True
