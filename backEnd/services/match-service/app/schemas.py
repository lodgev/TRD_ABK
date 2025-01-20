from pydantic import BaseModel
from datetime import date, datetime

class Club(BaseModel):
    id: int
    rank: int
    club: str
    country: str
    level: str
    elo: float
    start_date: date
    end_date: date

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
