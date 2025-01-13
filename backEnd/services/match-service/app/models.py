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


