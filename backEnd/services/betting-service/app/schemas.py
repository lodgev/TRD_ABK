from uuid import UUID

from pydantic import BaseModel
from decimal import Decimal
from typing import List, Optional
from datetime import datetime

class BetCreate(BaseModel):
    user_id: str
    match_id: int
    bet_type: str
    selected_team: str
    amount: Decimal
    coefficient: Decimal
    potential_win: Decimal
    

class BetUpdate(BaseModel):
    status: str = None
    amount: float = None
    selected_team: str = None
    coefficient: float = None
    potential_win: float = None

class CombinedBetDetailCreate(BaseModel):
    match_id: int
    bet_type: str
    # status: str = None
    selected_team: str = None
    coefficient: Decimal = None
    potential_win: Decimal = None

class CombinedBetCreate(BaseModel):
    user_id: UUID
    total_amount: Decimal
    details: List[CombinedBetDetailCreate]

class CombinedBetResponse(BaseModel):
    combined_bet_id: int
    user_id: UUID
    total_amount: Decimal
    total_odds: Decimal
    potential_win: Decimal
    status: str
    created_at: datetime
    details: List[CombinedBetDetailCreate]

    class Config:
        orm_mode = True
# class OddsUpdate(BaseModel):
#     home_coeff: Decimal
#     away_coeff: Decimal

# class BonusCreate(BaseModel):
#     user_id: str
#     bonus_amount: Decimal
#     expires_at: Optional[str]
