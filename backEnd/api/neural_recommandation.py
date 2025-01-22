import pandas as pd
import numpy as np
import streamlit as st
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Load feedback data
feedback_file_path = 'feedback.csv'
feedback_df = pd.read_csv(feedback_file_path)

# Prepare interaction matrix
def prepare_data(feedback_df):
    feedback_df = feedback_df[feedback_df['action'] == 'rated'].dropna(subset=['rating'])
    feedback_df['rating'] = feedback_df['rating'].astype(float)
    user_ids = feedback_df['user_id'].astype('category').cat.codes
    news_ids = feedback_df['news_id'].astype('category').cat.codes
    feedback_df['user_id'] = user_ids
    feedback_df['news_id'] = news_ids

    num_users = user_ids.max() + 1
    num_items = news_ids.max() + 1
    return feedback_df, num_users, num_items

feedback_df, num_users, num_items = prepare_data(feedback_df)

# Split into train and test sets
train_df, test_df = train_test_split(feedback_df, test_size=0.2, random_state=42)

# Define Dataset
class FeedbackDataset(Dataset):
    def __init__(self, df):
        self.users = torch.tensor(df['user_id'].values, dtype=torch.long)
        self.items = torch.tensor(df['news_id'].values, dtype=torch.long)
        self.ratings = torch.tensor(df['rating'].values, dtype=torch.float)

    def __len__(self):
        return len(self.ratings)

    def __getitem__(self, idx):
        return self.users[idx], self.items[idx], self.ratings[idx]

train_dataset = FeedbackDataset(train_df)
test_dataset = FeedbackDataset(test_df)

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

# Define Neural Collaborative Filtering Model
class NCF(nn.Module):
    def __init__(self, num_users, num_items, embedding_dim=50):
        super(NCF, self).__init__()
        self.user_embedding = nn.Embedding(num_users, embedding_dim)
        self.item_embedding = nn.Embedding(num_items, embedding_dim)

        self.fc_layers = nn.Sequential(
            nn.Linear(embedding_dim * 2, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )

    def forward(self, user_ids, item_ids):
        user_embed = self.user_embedding(user_ids)
        item_embed = self.item_embedding(item_ids)
        x = torch.cat([user_embed, item_embed], dim=-1)
        return self.fc_layers(x).squeeze()

model = NCF(num_users, num_items)
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# Train the model
def train(model, train_loader, criterion, optimizer, epochs=10):
    model.train()
    for epoch in range(epochs):
        total_loss = 0
        for user_ids, item_ids, ratings in train_loader:
            optimizer.zero_grad()
            predictions = model(user_ids, item_ids)
            loss = criterion(predictions, ratings)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        print(f"Epoch {epoch + 1}, Loss: {total_loss / len(train_loader)}")

# Evaluate the model
def evaluate(model, test_loader):
    model.eval()
    predictions, targets = [], []
    with torch.no_grad():
        for user_ids, item_ids, ratings in test_loader:
            preds = model(user_ids, item_ids)
            predictions.extend(preds.numpy())
            targets.extend(ratings.numpy())
    rmse = mean_squared_error(targets, predictions, squared=False)
    print(f"Test RMSE: {rmse}")
    return rmse

train(model, train_loader, criterion, optimizer, epochs=10)
evaluate(model, test_loader)

# Generate recommendations for a user
def recommend_for_user(model, user_id, num_recommendations=10):
    model.eval()
    all_items = torch.arange(num_items, dtype=torch.long)
    user_ids = torch.full((num_items,), user_id, dtype=torch.long)
    with torch.no_grad():
        predictions = model(user_ids, all_items)
    top_items = predictions.argsort(descending=True)[:num_recommendations]
    return top_items.numpy()


def map_article_ids_to_content(recommendations, articles_df):
    """
    Maps recommended article IDs to their titles and content.
    """
    recommended_articles = articles_df.iloc[recommendations]
    return recommended_articles

# Load articles
ARTICLES_PATH = "news_test.csv"  # Path to your articles dataset
articles_df = pd.read_csv(ARTICLES_PATH)

# Define the Streamlit App
def app():
    st.title("Personalized News Recommendation System with NCF")

    # Load or retrain model
    model_path = "ncf_model.pth"
    try:
        model.load_state_dict(torch.load(model_path))
        st.success("Model loaded successfully.")
    except FileNotFoundError:
        st.warning("Model not found. Training a new one...")
        train(model, train_loader, criterion, optimizer, epochs=10)
        torch.save(model.state_dict(), model_path)
        st.success("Model trained and saved.")

    # Select User
    user_id = st.selectbox("Select User ID", feedback_df['user_id'].unique())
    
    # Generate Recommendations
    if st.button("Get Recommendations"):
        recommendations = recommend_for_user(model, user_id)
        recommended_articles = map_article_ids_to_content(recommendations, articles_df)
        
        st.write("### Recommended Articles")
        for _, row in recommended_articles.iterrows():
            st.write(f"#### {row['Title']}")
            st.image(row['Image'], width=300)
            st.write(row['Content'])
            st.markdown("---")

if __name__ == "__main__":
    app()

""" # Example: Recommend top 10 articles for user 0
user_id = 0
recommendations = recommend_for_user(model, user_id)
print(f"Top recommendations for user {user_id}: {recommendations}") """
