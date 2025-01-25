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
    user_id: UUID
    match_id: int
    bet_type: str
    selected_team: str
    amount: Decimal
    coefficient: Decimal
    potential_win: Decimal

# class BetCreate(BaseModel):
#     user_id: UUID  # Убедитесь, что используете правильный UUID тип
#     match_id: str
#     bet_type: str
#     amount: float
#     selected_team: str
#     coefficient: condecimal(max_digits=10, decimal_places=2)
#     potential_win: condecimal(max_digits=10, decimal_places=2)

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
