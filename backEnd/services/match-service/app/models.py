# classes from db
from sqlalchemy import Column, Integer, String, Float, Date
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

class Match(Base):
    __tablename__ = "matches"

    match_id = Column(Integer, primary_key=True, index=True)
    rank = Column(Integer, index=True)
    club = Column(String, index=True)
    country = Column(String, index=True)
    level = Column(String, index=True)
    elo = Column(Float, index=True)
    start_date = Column(Date, index=True)
    end_date = Column(Date, index=True)

#    BIGINT PRIMARY KEY,
#     home_team VARCHAR(255) NOT NULL,
#     home_score INT NOT NULL,
#     away_team VARCHAR(255) NOT NULL,
#     away_score INT NOT NULL,
#     score_string VARCHAR(20),
#     match_date TIMESTAMP NOT NULL
