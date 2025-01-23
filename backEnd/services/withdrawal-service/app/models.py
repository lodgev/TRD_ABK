# # classes from db
# from sqlalchemy import Column, Integer, String, Float, Date
# from .database import Base
#
# class Club(Base):
#     __tablename__ = "clubs"
#
#     id = Column(Integer, primary_key=True, index=True)
#     rank = Column(Integer, index=True)
#     club = Column(String, index=True)
#     country = Column(String, index=True)
#     level = Column(String, index=True)
#     elo = Column(Float, index=True)
#     start_date = Column(Date, index=True)
#     end_date = Column(Date, index=True)
#
# class Match(Base):
#     __tablename__ = "matches"
#
#     match_id = Column(Integer, primary_key=True, index=True)
#     home_team = Column(String, index=True)
#     home_score = Column(Integer)
#     away_team = Column(String, index=True)
#     away_score = Column(Integer)
#     score_string = Column(String, index=True)
#     match_date = Column(Date, index=True)
#     home_coeff = Column(Float, index=True)
#     away_coeff = Column(Float, index=True)
#

from sqlalchemy import Column, Integer, Float, String, DateTime, func, Enum
from app.database import Base
#
# class Transaction(Base):
#     __tablename__ = "transactions"
#
#     id = Column(Integer, primary_key=True, index=True)
#     wallet_id = Column(Integer, nullable=False)
#     amount = Column(Float, nullable=False)
#     transaction_type = Column(Enum("deposit", "withdrawal", name="transaction_type_enum"), nullable=False)  # 'deposit' or 'withdrawal'
#     status = Column(Enum("pending", "completed", "failed", name="status_enum"), default="pending")  # 'pending', 'completed', 'failed'
#     created_at = Column(DateTime, default=func.now())
#     updated_at = Column(DateTime, default=func.now())

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    wallet_id = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    transaction_type = Column(String, nullable=False)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())



# CREATE TABLE transactions (
#     id SERIAL PRIMARY KEY,
#     wallet_id INT NOT NULL REFERENCES wallets(id) ON DELETE CASCADE,
#     amount DECIMAL(15, 2) NOT NULL,
#     transaction_type VARCHAR(10) CHECK (transaction_type IN ('deposit', 'withdrawal')),
#     status VARCHAR(20) CHECK (status IN ('pending', 'completed', 'failed')),
#     created_at TIMESTAMP DEFAULT NOW(),
#     updated_at TIMESTAMP DEFAULT NOW()
# );
