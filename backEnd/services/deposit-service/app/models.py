

from sqlalchemy import Column, Integer, Float, String, DateTime, func, Enum
from app.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    wallet_id = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    transaction_type = Column(Enum("deposit", "withdrawal", name="transaction_type_enum"), nullable=False)  # 'deposit' or 'withdrawal'
    status = Column(Enum("pending", "completed", "failed", name="status_enum"), default="pending")  # 'pending', 'completed', 'failed'
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
