# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# import os
#
# DATABASE_URL = (
#     f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
#     f"@wallet-db/{os.getenv('POSTGRES_DB')}"
# )
#
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
# Base = declarative_base()
#
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

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

# Подключение ко второй базе данных (betts-db)
BETTS_DATABASE_URL = (
    f"postgresql+psycopg2://{os.getenv('POSTGRES_USER_BETTS')}:{os.getenv('POSTGRES_PASSWORD_BETTS')}"
    f"@betting-db/{os.getenv('POSTGRES_DB_BETTS')}"
)

betts_engine = create_engine(BETTS_DATABASE_URL)
BettsSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=betts_engine)

# Базовые классы моделей для каждой БД
WalletBase = declarative_base()
BettsBase = declarative_base()

# Функции для получения сессии каждой базы данных
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
