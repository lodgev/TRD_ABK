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


# === odds ===



def calculate_odds(elo_a: float, elo_b: float):
    prob_a = 1 / (1 + 10 ** ((elo_b - elo_a) / 400))
    prob_b = 1 - prob_a
    prob_draw = 0.20
    prob_a = prob_a * (1 - prob_draw)
    prob_b = prob_b * (1 - prob_draw)

    return {
        "home_win": round(prob_a, 4),
        "draw": round(prob_draw, 4),
        "away_win": round(prob_b, 4)
    }

def add_odds(db: Session, match_id: int):
    match = db.query(models.Match).filter(models.Match.match_id == match_id).first()
    if not match:
        return None
    home_club = db.query(models.Club).filter(models.Club.club == match.home_team).first()
    away_club = db.query(models.Club).filter(models.Club.club == match.away_team).first()

    if not home_club or not away_club:
        return None

    odds_data = calculate_odds(home_club.elo, away_club.elo)

    odds = models.Odds(
        match_id=match_id,
        home_win=odds_data["home_win"],
        draw=odds_data["draw"],
        away_win=odds_data["away_win"],
    )
    db.add(odds)
    db.commit()
    db.refresh(odds)

    return odds


def update_odds(db: Session, match_id: int):
    match = db.query(models.Match).filter(models.Match.match_id == match_id).first()
    if not match:
        return None

    home_club = db.query(models.Club).filter(models.Club.club == match.home_team).first()
    away_club = db.query(models.Club).filter(models.Club.club == match.away_team).first()

    if not home_club or not away_club:
        return None

    odds_data = calculate_odds(home_club.elo, away_club.elo)

    odds = db.query(models.Odds).filter(models.Odds.match_id == match_id).first()

    if not odds:
        odds = models.Odds(
            match_id=match_id,
            home_win=odds_data["home_win"],
            draw=odds_data["draw"],
            away_win=odds_data["away_win"],
        )
        db.add(odds)
    else:
        odds.home_win = odds_data["home_win"]
        odds.draw = odds_data["draw"]
        odds.away_win = odds_data["away_win"]

    db.commit()
    db.refresh(odds)

    return odds
