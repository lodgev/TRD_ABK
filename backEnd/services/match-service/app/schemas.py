from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class Club(BaseModel):
    id: int
    rank: int
    club: str
    country: str
    level: str
    elo: float
    start_date: date
    end_date: date
    likes: int
    
    
class LikeDislikeRequest(BaseModel):
    action: str


class Match(BaseModel):
    match_id: int
    home_team: str
    home_score: int
    away_team: str
    away_score: int
    score_string: str
    match_date: datetime
    home_coeff: float
    away_coeff: float


class MatchCreate(BaseModel):
    home_team: str
    home_score: int
    away_team: str
    away_score: int
    score_string: str
    match_date: datetime
    home_coeff: float
    away_coeff: float

class MatchUpdate(BaseModel):
    home_team: Optional[str] = None
    home_score: Optional[int] = None
    away_team: Optional[str] = None
    away_score: Optional[int] = None
    score_string: Optional[str] = None
    match_date: Optional[datetime] = None
    home_coeff: Optional[float] = None
    away_coeff: Optional[float] = None


class Odds(BaseModel):
    match_id: int
    home_win: float
    draw: float
    away_win: float

class OddsCreate(BaseModel):
    match_id: int
    home_win: float
    draw: float
    away_win: float

    class Config:
        orm_mode = True

