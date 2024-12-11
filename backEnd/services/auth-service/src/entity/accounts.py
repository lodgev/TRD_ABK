from sqlalchemy import Column, String, Integer, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Account(Base):
    __tablename__ = "Accounts"  

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))  # UUID primary key
    
    login = Column(String, unique=True, nullable=False)  
    password = Column(String, nullable=False)  
    
    role = Column(Integer, default=0)  
    
    # Tokens
    refresh_token = Column(String, unique=True, nullable=True) 
    registration_token = Column(String, unique=True, nullable=True) 
    
    # Dates
    registrated_at = Column(DateTime, nullable=True)  
    last_signed_in_at = Column(DateTime, nullable=True) 
    created_at = Column(DateTime, default=func.now()) 
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())  
    deleted_at = Column(DateTime, nullable=True) 
