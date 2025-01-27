# classes from db
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from .database import Base

class Club(Base):
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

class Match(Base):
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

class Odds(Base):
    __tablename__ = "odds"
    match_id = Column(Integer, ForeignKey("matches.match_id"), primary_key=True)
    home_win = Column(Float, nullable=False)
    draw = Column(Float, nullable=False)
    away_win = Column(Float, nullable=False)

