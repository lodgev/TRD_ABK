# routes for the API

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, schemas, database
router = APIRouter()

# === clubs ===

@router.get("/clubs", response_model=list[schemas.Club])
def get_clubs(db: Session = Depends(database.get_db)):
    return crud.get_clubs(db)

@router.get("/clubs/{club_id}", response_model=schemas.Club)
def get_club(club_id: int, db: Session = Depends(database.get_db)):
    club = crud.get_club_by_id(db, club_id)
    if not club:
        raise HTTPException(status_code=404, detail="Club not found")
    return club

# 
# @router.post("/clubs", response_model=schemas.Club)
# def create_club(club: schemas.ClubCreate, db: Session = Depends(database.get_db)):
#     return crud.create_club(db, club)

# @router.put("/clubs/{club_id}/update-likes", response_model=list[schemas.ClubUpdateResponse

@router.post("/clubs/{club_id}/update-likes")
async def update_likes(club_id: int, data: schemas.LikeDislikeRequest, db: Session = Depends(database.get_db)):
    club = crud.update_likes(db, club_id, data.action)
    return club


# === matches ===
@router.get("/matches", response_model=list[schemas.Match])
def get_matches(db: Session = Depends(database.get_db)):
    return crud.get_matches(db)

@router.get("/matches/{match_id}", response_model=schemas.Match)
def get_match(match_id: int, db: Session = Depends(database.get_db)):
    match = crud.get_match_by_id(db, match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return match

# === matches ===

@router.post("/matches", response_model=schemas.Match)
def add_match(match: schemas.MatchCreate, db: Session = Depends(database.get_db)):
    return crud.add_match(db, match)

@router.put("/matches/{match_id}", response_model=schemas.Match)
def update_match(match_id: int, match: schemas.MatchUpdate, db: Session = Depends(database.get_db)):
    updated_match = crud.update_match(db, match_id, match)
    if not updated_match:
        raise HTTPException(status_code=404, detail="Match not found")
    return updated_match

@router.delete("/matches/{match_id}", response_model=schemas.Match)
def cancel_match(match_id: int, db: Session = Depends(database.get_db)):
    deleted_match = crud.cancel_match(db, match_id)
    if not deleted_match:
        raise HTTPException(status_code=404, detail="Match not found")
    return deleted_match

# not working
# @router.get("/matches/date/{date}", response_model=list[schemas.Match])
# def get_matches_by_date(date: str, db: Session = Depends(database.get_db)):
#     return crud.get_matches_by_date(db, date)

# === odds ===

@router.post("/odds", response_model=schemas.Odds)
def add_odds(odds: schemas.OddsCreate, db: Session = Depends(database.get_db)):
    return crud.add_odds(db, odds.match_id)

@router.put("/odds/{match_id}", response_model=schemas.Odds)
def update_odds(match_id: int, db: Session = Depends(database.get_db)):
    # Call the CRUD function to recalculate and update the odds
    updated_odds = crud.update_odds(db, match_id)
    if not updated_odds:
        raise HTTPException(status_code=404, detail="Odds not found for the match")
    return updated_odds

# === odds ===

@router.get("/odds", response_model=list[schemas.Odds])
def get_all_odds(db: Session = Depends(database.get_db)):
    return crud.get_all_odds(db)

@router.delete("/odds/{match_id}")
def suppress_odd_for_match(match_id: int, db: Session = Depends(database.get_db)):
    success = crud.suppress_odd_for_match(db, match_id)
    if not success:
        raise HTTPException(status_code=404, detail="Odds not found for the match")
    return {"message": "Odds successfully deleted"}

@router.get("/odds/{match_id}", response_model=schemas.Odds)
def get_odd_for_match(match_id: int, db: Session = Depends(database.get_db)):
    odds = crud.get_odd_for_match(db, match_id)
    if not odds:
        raise HTTPException(status_code=404, detail="Odds not found for the match")
    return odds

@router.put("/odds")
def update_all_odds(db: Session = Depends(database.get_db)):
    updated_odds = crud.update_all_odds(db)
    if not updated_odds:
        raise HTTPException(status_code=404, detail="No matches found or no odds updated")
    return updated_odds
