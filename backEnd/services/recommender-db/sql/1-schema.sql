CREATE TABLE feedback (
    timestamp TIMESTAMP PRIMARY KEY DEFAULT CURRENT_TIMESTAMP,
    user_id UUID NOT NULL,
    news_id VARCHAR(255) NOT NULL,
    action VARCHAR(50) NOT NULL,
    rating INT
);

CREATE TABLE IF NOT EXISTS user_actions (
    click_id SERIAL PRIMARY KEY,
    club_id INTEGER NOT NULL,
    user_id UUID NOT NULL,
    action VARCHAR(50) NOT NULL CHECK (action IN ('liked', 'disliked')),
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sport_news (
    team_id INTEGER NOT NULL,
    news_id VARCHAR(255) PRIMARY KEY,
    title TEXT NOT NULL,
    image_url TEXT,
    published_time TIMESTAMP NOT NULL,
    source TEXT NOT NULL,
    url TEXT NOT NULL,
    content TEXT
);