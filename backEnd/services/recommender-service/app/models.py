from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, DateTime, Text, Time, Boolean, Enum, DECIMAL, \
    Float, Date
from sqlalchemy.dialects.postgresql import UUID
from app.database import RecommenderBase, UserBase, MatchBase, BettingBase
from datetime import datetime

from sqlalchemy.orm import relationship


class UserAction(RecommenderBase):
    __tablename__ = "user_actions"

    click_id = Column(Integer, primary_key=True, index=True)
    club_id = Column(Integer, nullable=False)
    user_id = Column(UUID, nullable=False)
    action = Column(String(50), nullable=False)
    timestamp = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)


class Feedback(RecommenderBase):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID, nullable=False, index=True)
    news_id = Column(UUID, nullable=False, index=True)
    action = Column(String(50), nullable=False, index=True)
    rating = Column(Integer, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)


class SportNews(RecommenderBase):
    __tablename__ = "sport_news"

    news_id = Column(String, primary_key=True, index=True)
    team_id = Column(Integer, nullable=False)
    title = Column(Text, nullable=False)
    image_url = Column(Text, nullable=True)
    published_time = Column(DateTime, nullable=False)
    source = Column(String, nullable=False)
    url = Column(Text, nullable=False)
    content = Column(Text, nullable=True)


# ------------------

class User(UserBase):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    refreshtoken = Column(String)
    createdat = Column(Time)
    updatedat = Column(Time, nullable=True)
    lastsigninat = Column(Time, nullable=True)
    firstname = Column(String)
    lastname = Column(String)
    is_verified = Column(Boolean, default=False)
    reset_token = Column(String)
    reset_token_expiration = Column(Time)


class Bet(BettingBase):
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




class CombinedBet(BettingBase):
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

class CombinedBetDetail(BettingBase):
    __tablename__ = "combined_bet_details"

    detail_id = Column(Integer, primary_key=True, autoincrement=True)
    combined_bet_id = Column(Integer, ForeignKey("combined_bets.combined_bet_id"))
    match_id = Column(Integer, nullable=False)
    bet_type = Column(String(50), nullable=False)
    selected_team = Column(String(255), nullable=False)
    coefficient = Column(DECIMAL(5,2), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)

    combined_bet = relationship("CombinedBet", back_populates="details")



class Club(MatchBase):
    __tablename__ = "clubs"

    id = Column(Integer, primary_key=True, index=True)
    rank = Column(Integer, index=True)
    club = Column(String, index=True)
    country = Column(String, index=True)
    level = Column(String, index=True)
    elo = Column(Float, index=True)
    start_date = Column(Date, index=True)
    end_date = Column(Date, index=True)
    likes = Column(Integer, index=True)

class Match(MatchBase):
    __tablename__ = "matches"

    match_id = Column(Integer, primary_key=True, index=True)
    home_team = Column(String, index=True)
    home_score = Column(Integer)
    away_team = Column(String, index=True)
    away_score = Column(Integer)
    score_string = Column(String, index=True)
    match_date = Column(Date, index=True)
    home_coeff = Column(Float, index=True)
    away_coeff = Column(Float, index=True)

class Odds(MatchBase):
    __tablename__ = "odds"
    match_id = Column(Integer, ForeignKey("matches.match_id"), primary_key=True)
    home_win = Column(Float, nullable=False)
    draw = Column(Float, nullable=False)
    away_win = Column(Float, nullable=False)
