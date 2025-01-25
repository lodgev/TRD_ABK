CREATE TABLE IF NOT EXISTS user_actions (
    click_id SERIAL PRIMARY KEY,
    club_id INTEGER NOT NULL,
    user_id UUID NOT NULL,
    action VARCHAR(50) NOT NULL CHECK (action IN ('liked', 'disliked', 'commented')),
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

`


