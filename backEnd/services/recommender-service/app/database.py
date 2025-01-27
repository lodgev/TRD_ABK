# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# import os
#
# # Define connection URLs for each database
# DATABASES = {
#     "recommender": f"postgresql+psycopg2://{os.getenv('RECOMMENDER_DB_USER')}:{os.getenv('RECOMMENDER_DB_PASSWORD')}@recommender-db/{os.getenv('RECOMMENDER_DB')}",
#     "user": f"postgresql+psycopg2://{os.getenv('USER_DB_USER')}:{os.getenv('USER_DB_PASSWORD')}@user-db/{os.getenv('USER_DB')}",
#     "match": f"postgresql+psycopg2://{os.getenv('MATCH_DB_USER')}:{os.getenv('MATCH_DB_PASSWORD')}@match-db/{os.getenv('MATCH_DB')}",
#     "betting": f"postgresql+psycopg2://{os.getenv('BETTING_DB_USER')}:{os.getenv('BETTING_DB_PASSWORD')}@betting-db/{os.getenv('BETTING_DB')}",
# }
#
# engine = create_engine(DATABASES["recommender"])
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()
#
# # Additional engines and sessions for other databases
# additional_engines = {key: create_engine(url) for key, url in DATABASES.items() if key != "recommender"}
# additional_sessions = {key: sessionmaker(autocommit=False, autoflush=False, bind=engine) for key, engine in additional_engines.items()}
#
# # Function to get the session for the primary database
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#
# # Function to get the session for a specific additional database
# def get_additional_db(db_name: str):
#     if db_name not in additional_sessions:
#         raise ValueError(f"Database '{db_name}' is not configured.")
#     db = additional_sessions[db_name]()
#     try:
#         yield db
#     finally:
#         db.close()

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database connection URLs
RECOMMENDER_DATABASE_URL = (
    f"postgresql+psycopg2://{os.getenv('RECOMMENDER_DB_USER')}:{os.getenv('RECOMMENDER_DB_PASSWORD')}"
    f"@recommender-db/{os.getenv('RECOMMENDER_DB')}"
)

USER_DATABASE_URL = (
    f"postgresql+psycopg2://{os.getenv('USER_DB_USER')}:{os.getenv('USER_DB_PASSWORD')}"
    f"@user-db/{os.getenv('USER_DB')}"
)

MATCH_DATABASE_URL = (
    f"postgresql+psycopg2://{os.getenv('MATCH_DB_USER')}:{os.getenv('MATCH_DB_PASSWORD')}"
    f"@match-db/{os.getenv('MATCH_DB')}"
)

BETTING_DATABASE_URL = (
    f"postgresql+psycopg2://{os.getenv('BETTING_DB_USER')}:{os.getenv('BETTING_DB_PASSWORD')}"
    f"@betting-db/{os.getenv('BETTING_DB')}"
)

# Create database engines
recommender_engine = create_engine(RECOMMENDER_DATABASE_URL)
user_engine = create_engine(USER_DATABASE_URL)
match_engine = create_engine(MATCH_DATABASE_URL)
betting_engine = create_engine(BETTING_DATABASE_URL)

# Session factories
RecommenderSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=recommender_engine)
UserSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=user_engine)
MatchSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=match_engine)
BettingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=betting_engine)

# Base classes for models
RecommenderBase = declarative_base()
UserBase = declarative_base()
MatchBase = declarative_base()
BettingBase = declarative_base()

# Dependency injection functions
def get_recommender_db():
    db = RecommenderSessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_db():
    db = UserSessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_match_db():
    db = MatchSessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_betting_db():
    db = BettingSessionLocal()
    try:
        yield db
    finally:
        db.close()
