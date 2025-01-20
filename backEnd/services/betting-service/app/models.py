from sqlalchemy import Column, Integer, String, DECIMAL, Enum, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base 

class Bet(Base):
    __tablename__ = "bets" 

    bet_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    match_id = Column(Integer, nullable=False)
    bet_type = Column(Enum("win", "lose", "draw", name="bet_type_enum"), nullable=False)
    selected_team = Column(String(255), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    potential_win = Column(DECIMAL(10, 2), nullable=False)
    coefficient = Column(DECIMAL(5, 2), nullable=False)
    status = Column(Enum("waiting_list", "pending", "won", "lost", name="status_enum"), default="waiting_list")
    created_at = Column(TIMESTAMP, nullable=False)

