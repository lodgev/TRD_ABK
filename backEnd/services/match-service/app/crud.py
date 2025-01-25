from sqlalchemy.orm import Session
from . import models, schemas

# === clubs ===
def get_clubs(db: Session):
    return db.query(models.Club).all()

def get_club_by_id(db: Session, club_id: int):
    return db.query(models.Club).filter(models.Club.id == club_id).first()

def update_likes(db: Session, club_id: int, action: str):
    club = db.query(models.Club).filter(models.Club.id == club_id).first()
    if not club:
        return None

    if action == "like":
        club.likes += 1
    elif action == "dislike":
        club.likes -= 1

    db.commit()
    db.refresh(club)
    return club

# === matches ===

def get_matches(db: Session):
    return db.query(models.Match).all()

def get_match_by_id(db: Session, match_id: int):
    return db.query(models.Match).filter(models.Match.match_id == match_id).first()


# === matches ===

def add_match(db: Session, match: schemas.MatchCreate):
    new_match = models.Match(
        home_team=match.home_team,
        home_score=match.home_score,
        away_team=match.away_team,
        away_score=match.away_score,
        score_string=match.score_string,
        match_date=match.match_date,
        home_coeff=match.home_coeff,
        away_coeff=match.away_coeff,
    )
    db.add(new_match)
    db.commit()
    db.refresh(new_match)
    return new_match

def update_match(db: Session, match_id: int, updated_match: schemas.MatchUpdate):
    match = db.query(models.Match).filter(models.Match.match_id == match_id).first()
    if not match:
        return None
    
    for key, value in updated_match.dict(exclude_unset=True).items():
        setattr(match, key, value)
    
    db.commit()
    db.refresh(match)
    return match

def cancel_match(db: Session, match_id: int):
    match = db.query(models.Match).filter(models.Match.match_id == match_id).first()
    if not match:
        return None
    
    db.delete(match)
    db.commit()
    return match



