# crud - create read update delete 
# describe all post/get etc request in code

from sqlalchemy.orm import Session
from . import models, schemas

# === clubs ===
def get_clubs(db: Session):
    return db.query(models.Club).all()

def get_club_by_id(db: Session, club_id: int):
    return db.query(models.Club).filter(models.Club.id == club_id).first()

# === matches ===

def get_matches(db: Session):
    return db.query(models.Match).all()

def get_match_by_id(db: Session, match_id: int):
    return db.query(models.Match).filter(models.Match.match_id == match_id).first()




