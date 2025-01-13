from pydantic import BaseModel
from datetime import date

class Club(BaseModel):
    id: int
    rank: int
    club: str
    country: str
    level: str
    elo: float
    start_date: date
    end_date: date


