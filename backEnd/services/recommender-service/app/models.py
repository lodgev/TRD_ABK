from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
from datetime import datetime


class UserAction(Base):
    __tablename__ = "user_actions"

    click_id = Column(Integer, primary_key=True, index=True)
    club_id = Column(Integer, nullable=False)
    user_id = Column(UUID, nullable=False)
    action = Column(String(50), nullable=False)
    timestamp = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID, nullable=False, index=True)
    news_id = Column(UUID, nullable=False, index=True)
    action = Column(String(50), nullable=False, index=True)
    rating = Column(Integer, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)


class SportNews(Base):
    __tablename__ = "sport_news"

    news_id = Column(String, primary_key=True, index=True)
    team_id = Column(Integer, nullable=False)
    title = Column(Text, nullable=False)
    image_url = Column(Text, nullable=True)
    published_time = Column(DateTime, nullable=False)
    source = Column(String, nullable=False)
    url = Column(Text, nullable=False)
    content = Column(Text, nullable=True)
