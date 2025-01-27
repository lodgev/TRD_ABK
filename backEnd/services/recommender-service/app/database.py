from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Define connection URLs for each database
DATABASES = {
    "recommender": f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@recommender-db/{os.getenv('POSTGRES_DB')}",
    "user": f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@user-db/{os.getenv('POSTGRES_DB')}",
    "match": f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@match-db/{os.getenv('POSTGRES_DB')}",
    "betting": f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@betting-db/{os.getenv('POSTGRES_DB')}"
}



engine = create_engine(DATABASES["recommender"])
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Additional engines and sessions for other databases
additional_engines = {key: create_engine(url) for key, url in DATABASES.items() if key != "recommender"}
additional_sessions = {key: sessionmaker(autocommit=False, autoflush=False, bind=engine) for key, engine in additional_engines.items()}

# Function to get the session for the primary database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to get the session for a specific additional database
def get_additional_db(db_name: str):
    if db_name not in additional_sessions:
        raise ValueError(f"Database '{db_name}' is not configured.")
    db = additional_sessions[db_name]()
    try:
        yield db
    finally:
        db.close()
