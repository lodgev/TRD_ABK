
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

WALLET_DATABASE_URL = (
    f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@wallet-db/{os.getenv('POSTGRES_DB')}"
)

wallet_engine = create_engine(WALLET_DATABASE_URL)
WalletSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=wallet_engine)

BETTS_DATABASE_URL = (
    f"postgresql+psycopg2://{os.getenv('POSTGRES_USER_BETTS')}:{os.getenv('POSTGRES_PASSWORD_BETTS')}"
    f"@betting-db/{os.getenv('POSTGRES_DB_BETTS')}"
)

betts_engine = create_engine(BETTS_DATABASE_URL)
BettsSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=betts_engine)

WalletBase = declarative_base()
BettsBase = declarative_base()

def get_wallet_db():
    db = WalletSessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_betts_db():
    db = BettsSessionLocal()
    try:
        yield db
    finally:
        db.close()
