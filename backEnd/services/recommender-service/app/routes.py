from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_recommender_db, get_user_db, get_match_db, get_betting_db
from datetime import datetime
from uuid import UUID
import pandas as pd

router = APIRouter()

# === Feedback Routes ===

@router.get("/feedback", response_model=list[schemas.Feedback])
def get_all_feedback(db: Session = Depends(get_recommender_db)):
    """Retrieve all feedback records."""
    return crud.get_feedback(db)

@router.get("/feedback/{user_id}", response_model=list[schemas.Feedback])
def get_feedback_by_user(user_id: UUID, db: Session = Depends(get_recommender_db)):
    """Retrieve feedback for a specific user."""
    feedback = crud.get_feedback_by_user(db, user_id)
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found for this user")
    return feedback

@router.post("/feedback", response_model=schemas.Feedback)
def create_feedback_entry(feedback: schemas.FeedbackCreate, db: Session = Depends(get_recommender_db)):
    """Create a new feedback entry."""
    feedback.timestamp = datetime.utcnow()
    return crud.create_feedback(db, feedback)

@router.get("/recommendations/{user_id}")
# def get_recommendations(user_id: UUID, db: Session = Depends(get_recommender_db)):
def get_recommendations(user_id: UUID, recommender_db: Session = Depends(get_recommender_db),
                            betting_db: Session = Depends(get_betting_db)):

    """Provide recommendations for a user."""
    try:
        # Fetch all sport news directly from the database
        # sport_news = crud.get_all_sport_news(recommender_db)
        # if not sport_news:
        #     raise HTTPException(status_code=404, detail="No sport news available")
        #
        # # Convert sport news into a DataFrame
        # news_df = pd.DataFrame([{
        #     "Team ID": news.team_id,
        #     "News ID": news.news_id,
        #     "Title": news.title,
        #     "Image": news.image_url,
        #     "Published Time": news.published_time,
        #     "Source": news.source,
        #     "URL": news.url,
        #     "Content": news.content
        # } for news in sport_news])
        #
        # # Preprocess the DataFrame
        # news_df = news_df.dropna(subset=["Content", "Title"])
        # news_df["Content"] = news_df["Content"].fillna("")

        # Generate recommendations
        recommendations = crud.recommend_articles(recommender_db, betting_db, user_id)
        if not recommendations:
            raise HTTPException(
                status_code=404, detail="No recommendations found for this user"
            )
        return {"recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")


# === User Action Routes ===

@router.post("/actions/", response_model=schemas.UserActionResponse)
def handle_user_action(action: schemas.UserActionCreate, db: Session = Depends(get_recommender_db)):
    """Handle a user's action on a team."""
    try:
        return crud.create_user_action(db, action)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing action: {str(e)}")

@router.get("/actions/user/{user_id}", response_model=list[schemas.UserActionResponse])
def get_user_actions(user_id: UUID, db: Session = Depends(get_recommender_db)):
    """Retrieve all actions by a specific user."""
    return crud.get_user_actions_by_user(db, user_id)

@router.get("/actions/club/{club_id}", response_model=list[schemas.UserActionResponse])
def get_club_actions(club_id: int, db: Session = Depends(get_recommender_db)):
    """Retrieve all actions related to a specific club."""
    return crud.get_user_actions_by_club(db, club_id)