from pydantic import BaseModel
from decimal import Decimal

class BetCreate(BaseModel):
    user_id: str
    match_id: int
    bet_type: str
    selected_team: str
    amount: Decimal
    coefficient: Decimal
    potential_win: Decimal
    

# class BetUpdate(BaseModel):
#     status: str

class BetUpdate(BaseModel):
    status: str = None
    amount: float = None
    selected_team: str = None
    coefficient: float = None
    potential_win: float = None

# class OddsUpdate(BaseModel):
#     home_coeff: Decimal
#     away_coeff: Decimal

# class BonusCreate(BaseModel):
#     user_id: str
#     bonus_amount: Decimal
#     expires_at: Optional[str]
