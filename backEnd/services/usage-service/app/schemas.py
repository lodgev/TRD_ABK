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
    user_id: UUID
    balance: float
    currency: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class WalletBalanceResponse(BaseModel):
    wallet_id: int
    balance: float
    currency: str


# ......................

class BetCreate(BaseModel):
    user_id: UUID
    match_id: int
    bet_type: str
    selected_team: str
    amount: Decimal
    coefficient: Decimal
    potential_win: Decimal


#
# class BetResponse(BetCreate):
#     id: int
#
#     class Config:
#         from_attributes = True
