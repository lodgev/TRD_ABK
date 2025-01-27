from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, database
from app.database import get_db
from datetime import datetime
from uuid import UUID
import pandas as pd

router = APIRouter()

# Initialize the DataFrame for news
try:
    news_df = pd.read_csv("news_test.csv", encoding="latin1")
    news_df = news_df.dropna(subset=["Content", "Title"])
    news_df["Content"] = news_df["Content"].fillna("")
except FileNotFoundError:
    raise RuntimeError("news_test.csv file not found. Ensure the file exists in the project directory.")
except Exception as e:
    raise RuntimeError(f"Error initializing news data: {e}")


# === Feedback Routes ===

@router.get("/feedback", response_model=list[schemas.Feedback])
def get_all_feedback(db: Session = Depends(get_db)):
    """Retrieve all feedback records."""
    return crud.get_feedback(db)

@router.get("/feedback/{user_id}", response_model=list[schemas.Feedback])
def get_feedback_by_user(user_id: UUID, db: Session = Depends(get_db)):
    """Retrieve feedback for a specific user."""
    feedback = crud.get_feedback_by_user(db, user_id)
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found for this user")
    return feedback

@router.post("/feedback", response_model=schemas.Feedback)
def create_feedback_entry(feedback: schemas.FeedbackCreate, db: Session = Depends(get_db)):
    """Create a new feedback entry."""
    feedback.timestamp = datetime.utcnow()
    return crud.create_feedback(db, feedback)

@router.get("/recommendations/{user_id}")
def get_recommendations(user_id: UUID, db: Session = Depends(get_db)):
    """Provide recommendations for a user."""
    try:
        recommendations = crud.recommend_articles(db, user_id, news_df)
        if not recommendations:
            raise HTTPException(
                status_code=404, detail="No recommendations found for this user"
            )
        return {"recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")


# === User Action Routes ===

@router.post("/actions/", response_model=schemas.UserActionResponse)
def handle_user_action(action: schemas.UserActionCreate, db: Session = Depends(get_db)):
    """Handle a user's action on a team."""
    try:
        return crud.create_user_action(db, action)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing action: {str(e)}")

@router.get("/actions/user/{user_id}", response_model=list[schemas.UserActionResponse])
def get_user_actions(user_id: UUID, db: Session = Depends(get_db)):
    """Retrieve all actions by a specific user."""
    return crud.get_user_actions_by_user(db, user_id)

@router.get("/actions/club/{club_id}", response_model=list[schemas.UserActionResponse])
def get_club_actions(club_id: int, db: Session = Depends(get_db)):
    """Retrieve all actions related to a specific club."""
    return crud.get_user_actions_by_club(db, club_id)


# === Sport News Routes ===

@router.post("/sport-news/process")
def process_and_insert_sport_news(db: Session = Depends(get_db)):
    """
    Read, preprocess, and insert articles from 'text_news.csv' into the sport_news table.
    Ensures no duplicate articles are added.
    """
    try:
        result = crud.insert_sport_news_from_csv(db, "text_news.csv")
        if result["status"] == "success":
            return {
                "message": f"Processed text_news.csv successfully.",
                "added_articles": result["added_articles"],
                "skipped_articles": result["skipped_articles"],
            }
        else:
            raise HTTPException(status_code=400, detail=result["message"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing sport news: {str(e)}")
