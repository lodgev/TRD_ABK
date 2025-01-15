# crud - create read update delete 
# describe all post/get etc request in code

from sqlalchemy.orm import Session
from . import models, schemas

def get_clubs(db: Session):
    return db.query(models.Club).all()

def get_club_by_id(db: Session, club_id: int):
    return db.query(models.Club).filter(models.Club.id == club_id).first()

# def get_matches(db: Session):
#     return db.query(models.Club).all()

# def get_match_by_id(db: Session, club_id: int):
#     return db.query(models.Club).filter(models.Club.id == club_id).first()


# def create_club(db: Session, club: schemas.ClubCreate):
#     db_club = models.Club(**club.dict())
#     db.add(db_club)
#     db.commit()
#     db.refresh(db_club)
#     return db_club
