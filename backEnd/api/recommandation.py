import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

# Load datasets
football_news_df = pd.read_csv('news_test.csv', encoding='latin1')
matches_df = pd.read_csv('matches.csv', encoding='latin1')
users_df = pd.read_csv('users.csv')
bets_df = pd.read_csv('bets.csv')

# Feedback storage in a CSV file
feedback_file_path = 'feedback.csv'
try:
    feedback_df = pd.read_csv(feedback_file_path)
except FileNotFoundError:
    feedback_df = pd.DataFrame(columns=['user_id', 'news_id', 'action', 'rating'])

# Preprocessing football news data
def preprocess_data(news_df):
    news_df = news_df.dropna(subset=['Content', 'Title'])
    news_df['Content'] = news_df['Content'].fillna('')
    return news_df

football_news_df = preprocess_data(football_news_df)

# Build recommendation system
def recommend_articles(user_id, football_news_df, bets_df, feedback_df, top_n=20):
    # Get user's bet preferences
    user_bets = bets_df[bets_df['user_id'] == user_id]
    preferred_teams = user_bets['selected_team'].unique()

    # Filter articles about preferred teams
    preferred_articles = football_news_df[football_news_df['Content'].str.contains('|'.join(preferred_teams), case=False, na=False)]

    # Exclude "Not Interested" articles
    not_interested = feedback_df[(feedback_df['user_id'] == user_id) & (feedback_df['action'] == 'not_interested')]['news_id'].tolist()
    filtered_articles = football_news_df[~football_news_df['News ID'].isin(not_interested)]

    # Use TF-IDF for content-based filtering
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(filtered_articles['Content'])

    # Compute similarity for all articles
    similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Adjust scores based on feedback
    user_feedback = feedback_df[feedback_df['user_id'] == user_id]
    for _, feedback in user_feedback.iterrows():
        if feedback['action'] == 'rated':
            # Boost articles similar to highly-rated ones
            news_index = filtered_articles[filtered_articles['News ID'] == feedback['news_id']].index[0]
            similarity_matrix[:, news_index] *= (1 + feedback['rating'] / 5.0)

    # Recommend top articles
    recommended_indices = similarity_matrix.sum(axis=1).argsort()[-top_n:][::-1]
    recommendations = filtered_articles.iloc[recommended_indices]

    return recommendations

# Streamlit app
def app():
    global feedback_df

    st.title("Sport News Recommendation System")

    # Check if a specific article is being read
    query_params = st.experimental_get_query_params()
    if "news_id" in query_params:
        # Display the full article content
        news_id = query_params["news_id"][0]
        user_id = query_params.get("user_id", [None])[0]
        article = football_news_df[football_news_df['News ID'] == news_id]
        if not article.empty:
            st.write(f"## {article.iloc[0]['Title']}")
            st.write(article.iloc[0]['Content'])
            rating = st.slider("Rate this article", 1, 5, key=f"rating_{news_id}")
            if rating:
                new_feedback = pd.DataFrame([{"user_id": user_id, "news_id": news_id, "action": "rated", "rating": rating}])
                feedback_df = pd.concat([feedback_df, new_feedback], ignore_index=True)
                feedback_df.to_csv(feedback_file_path, index=False)

            if st.button("Back to Main Page"):
                st.query_params.clear()
                st.experimental_set_query_params()
        return

    # User selection
    user_id = st.selectbox("Select User", users_df['id'])

    # Get recommendations
    recommendations = recommend_articles(user_id, football_news_df, bets_df, feedback_df)

    st.write("## Recommended Articles")
    for idx, row in recommendations.iterrows():
        st.write(f"### {row['Title']}")
        st.image(row['Image'])
        read_url = f"?news_id={row['News ID']}&user_id={user_id}"
        st.markdown(f"[Read the article]({read_url})")

        # Feedback buttons
        if st.button("Not Interested", key=f"not_interested_{user_id}_{idx}"):
            new_feedback = pd.DataFrame([{"user_id": user_id, "news_id": row['News ID'], "action": "not_interested", "rating": None}])
            feedback_df = pd.concat([feedback_df, new_feedback], ignore_index=True)
            feedback_df.to_csv(feedback_file_path, index=False)
            st.success("Marked as Not Interested")

# Run the app
if __name__ == "__main__":
    app()
