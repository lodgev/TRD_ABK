# routes for the API

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, schemas, database

router = APIRouter()


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
