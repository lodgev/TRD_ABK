CREATE TABLE bets (
    bet_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    match_id INT NOT NULL,
    amount NUMERIC(10, 2) NOT NULL,
    bet_type VARCHAR(10) NOT NULL,
    selected_team VARCHAR(100) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
