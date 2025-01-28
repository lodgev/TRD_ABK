from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from . import models, schemas
from app.models import UserAction
from app.schemas import UserActionCreate
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from uuid import UUID
import logging
# from app.database import get_additional_db


# Logger configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def recommend_articles(recommender_db: Session, betting_db: Session, user_id: UUID, top_n: int = 20):
    try:
        # Fetch feedback and bets for the user
        feedback = recommender_db.query(models.Feedback).filter(models.Feedback.user_id == user_id).all()

        bets = betting_db.query(models.Bet).filter(models.Bet.user_id == user_id).all()

        # Convert bets to DataFrame to extract preferred teams
        if not bets:
            logger.info("No bets or preferred teams found for user.")
            return []

        bets_df = pd.DataFrame([bet.__dict__ for bet in bets])
        if bets_df.empty or "selected_team" not in bets_df.columns:
            logger.info("No bets or preferred teams found for user.")
            return []

        preferred_teams = bets_df["selected_team"].unique()

        # Fetch all sport news from the database
        sport_news = recommender_db.query(models.SportNews).all()

        # Convert sport news to DataFrame
        news_df = pd.DataFrame([{
            "Team ID": news.team_id,
            "News ID": news.news_id,
            "Title": news.title,
            "Image": news.image_url,
            "Published Time": news.published_time,
            "Source": news.source,
            "URL": news.url,
            "Content": news.content
        } for news in sport_news])

        # Preprocess the DataFrame
        news_df = preprocess_data(news_df)

        # Filter articles about preferred teams
        preferred_articles = news_df[
            news_df["Content"].str.contains("|".join(preferred_teams), case=False, na=False)
        ]

        # Exclude articles the user has already interacted with
        interacted_articles = {f.news_id for f in feedback}
        filtered_articles = preferred_articles[
            ~preferred_articles["News ID"].isin(interacted_articles)
        ]

        if filtered_articles.empty:
            logger.info("No articles to recommend after filtering.")
            return []

        # Remove duplicate titles
        filtered_articles = filtered_articles.drop_duplicates(subset=["Title"])

        # Use TF-IDF for content-based filtering
        tfidf_vectorizer = TfidfVectorizer(stop_words="english")
        tfidf_matrix = tfidf_vectorizer.fit_transform(filtered_articles["Content"])

        # Compute similarity for all articles
        similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)

        # Adjust scores based on feedback
        for f in feedback:
            if f.action == "rated" and f.rating is not None:
                article_indices = filtered_articles[
                    filtered_articles["News ID"] == f.news_id
                ].index.tolist()
                if article_indices:
                    similarity_matrix[:, article_indices[0]] *= (1 + f.rating / 5.0)

        # Recommend top articles
        scores = similarity_matrix.sum(axis=1)
        top_indices = scores.argsort()[-top_n:][::-1]
        recommendations = filtered_articles.iloc[top_indices]

        return recommendations.to_dict(orient="records")

    except Exception as e:
        logger.error(f"Error recommending articles: {e}")
        return []


# Feedback CRUD operations
def get_feedback(db: Session):
    return db.query(models.Feedback).all()

def get_feedback_by_user(db: Session, user_id: UUID):
    return db.query(models.Feedback).filter(models.Feedback.user_id == user_id).all()

def create_feedback(db: Session, feedback: schemas.FeedbackCreate):
    try:
        db_feedback = models.Feedback(**feedback.dict())
        db.add(db_feedback)
        db.commit()
        db.refresh(db_feedback)
        return db_feedback
    except Exception as e:
        logger.error(f"Error creating feedback: {e}")
        db.rollback()
        raise

# UserAction CRUD operations
def create_user_action(db: Session, action_data: UserActionCreate):
    try:
        new_action = UserAction(**action_data.dict())
        db.add(new_action)
        db.commit()
        db.refresh(new_action)
        return new_action
    except Exception as e:
        logger.error(f"Error creating user action: {e}")
        db.rollback()
        raise

def get_user_actions_by_user(db: Session, user_id: UUID):
    return db.query(UserAction).filter(UserAction.user_id == user_id).all()

def get_user_actions_by_club(db: Session, club_id: int):
    return db.query(UserAction).filter(UserAction.club_id == club_id).all()

# SportNews CRUD operations
def get_all_sport_news(db: Session):
    return db.query(models.SportNews).all()

def create_sport_news(db: Session, sport_news: schemas.SportNewsCreate):
    try:
        db_sport_news = models.SportNews(**sport_news.dict())
        db.add(db_sport_news)
        db.commit()
        db.refresh(db_sport_news)
        return db_sport_news
    except Exception as e:
        logger.error(f"Error creating sport news: {e}")
        db.rollback()
        raise


def preprocess_data(news_df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess the news DataFrame:
    - Drops rows with missing Content or Title.
    - Fills missing Content with an empty string.
    """
    news_df = news_df.dropna(subset=["Content", "Title"])
    news_df["Content"] = news_df["Content"].fillna("")
    return news_df

