import streamlit as st
import requests

# Recommender Service Base URL
RECOMMENDER_SERVICE_URL = "http://recommender-service:80"

def show_news():
    """Display news articles and allow user feedback."""
    st.title("News Articles")

    # Get the user ID
    user_id = st.session_state.get("user_id")
    if not user_id:
        st.warning("Please log in to see personalized news recommendations.")
        return

    # Fetch recommendations
    try:
        response = requests.get(f"{RECOMMENDER_SERVICE_URL}/recommendations/{user_id}")
        if response.status_code == 200:
            recommendations = response.json().get("recommendations", [])
            if not recommendations:
                st.info("No news articles available for you at the moment.")
                return
        else:
            st.error("Failed to fetch news recommendations.")
            return
    except Exception as e:
        st.error(f"Error connecting to the recommender service: {str(e)}")
        return

    # Display each news article
    for idx, news in enumerate(recommendations):
        st.subheader(news["Title"])
        if news["Image"]:
            st.image(news["Image"], width=400)
        st.write(f"Published: {news['Published Time']}")
        st.write(f"Source: {news['Source']}")
        st.write(news["Content"][:500] + "...")  # Display a short preview
        st.markdown(f"[Read Full Article]({news['URL']})")

        # Rating slider
        rating = st.slider(f"Rate this article (0-5) for article {idx + 1}", 0, 5, key=f"rating_{news['News ID']}")
        if st.button(f"Submit Rating for Article {idx + 1}"):
            send_feedback(user_id, news["News ID"], "rated", rating)
        
        # Not Interested Button
        if st.button(f"Mark as Not Interested for Article {idx + 1}"):
            send_feedback(user_id, news["News ID"], "not_interested")


def send_feedback(user_id, news_id, action, rating=None):
    """Send feedback to the recommender service."""
    feedback_data = {
        "user_id": user_id,
        "news_id": news_id,
        "action": action,
        "rating": rating,
    }
    try:
        response = requests.post(f"{RECOMMENDER_SERVICE_URL}/feedback", json=feedback_data)
        if response.status_code == 200:
            st.success("Feedback submitted successfully.")
        else:
            st.error(f"Failed to submit feedback: {response.json().get('detail', 'Unknown error')}")
    except Exception as e:
        st.error(f"Error submitting feedback: {str(e)}")
