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

@router.put("/clubs/{club_id}/update-likes", response_model=list[schemas.ClubUpdateResponse])

def update_club_likes(club_id: int, action: str, db: Session = Depends(database.get_db)):
    if action not in ["like", "dislike"]:
        raise HTTPException(status_code=400, detail="Invalid action. Must be 'like' or 'dislike'.")

    updated_club = crud.update_likes(db, club_id, action)
    if not updated_club:
        raise HTTPException(status_code=404, detail="Club not found.")

    return {
        "club_id": updated_club.id,
        "club_name": updated_club.club,
        "likes": updated_club.likes,
        "dislikes": updated_club.dislikes,
    }


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


# not working
# @router.get("/matches/date/{date}", response_model=list[schemas.Match])
# def get_matches_by_date(date: str, db: Session = Depends(database.get_db)):
#     return crud.get_matches_by_date(db, date)