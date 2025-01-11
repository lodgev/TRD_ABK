from sqlalchemy import Column, String, DateTime, func
from app.database import Base
import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    refreshtoken = Column(String) 
    createdat = Column(String)
    updatedat = Column(String, nullable=True)
    lastsigninat = Column(String, nullable=True)
    firstname = Column(String)
    lastname = Column(String)
