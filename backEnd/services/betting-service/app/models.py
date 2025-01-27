from sqlalchemy import Column, Integer, String, DECIMAL, Enum, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
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




class CombinedBet(Base):
    __tablename__ = "combined_bets"

    combined_bet_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    total_amount = Column(DECIMAL(10,2), nullable=False)
    total_odds = Column(DECIMAL(10,4), nullable=False)
    potential_win = Column(DECIMAL(10,2), nullable=False)
    status = Column(String(50), nullable=False, default="waiting_list")
    created_at = Column(TIMESTAMP, nullable=False)

    # One-to-many relationship
    details = relationship("CombinedBetDetail", back_populates="combined_bet")

class CombinedBetDetail(Base):
    __tablename__ = "combined_bet_details"

    detail_id = Column(Integer, primary_key=True, autoincrement=True)
    combined_bet_id = Column(Integer, ForeignKey("combined_bets.combined_bet_id"))
    match_id = Column(Integer, nullable=False)
    bet_type = Column(String(50), nullable=False)
    selected_team = Column(String(255), nullable=False)
    coefficient = Column(DECIMAL(5,2), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)

    combined_bet = relationship("CombinedBet", back_populates="details")
