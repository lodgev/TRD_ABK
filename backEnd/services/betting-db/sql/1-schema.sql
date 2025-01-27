CREATE TYPE bet_type_enum AS ENUM ('win', 'lose', 'draw');
CREATE TYPE status_enum AS ENUM ('waiting_list', 'pending', 'won', 'lost');

CREATE TABLE bets (
    bet_id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL,
    match_id INT NOT NULL,
    bet_type bet_type_enum NOT NULL,
    selected_team VARCHAR(255) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    potential_win DECIMAL(10, 2) NOT NULL,
    coefficient DECIMAL(5, 2) NOT NULL,
    status status_enum DEFAULT 'waiting_list',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE combined_bets (
    combined_bet_id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    total_odds DECIMAL(10,4) NOT NULL,
    potential_win DECIMAL(10,2) NOT NULL,
    status VARCHAR(50) NOT NULL, 
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE combined_bet_details (
    detail_id SERIAL PRIMARY KEY,
    combined_bet_id INT NOT NULL REFERENCES combined_bets(combined_bet_id),
    match_id INT NOT NULL,
    bet_type VARCHAR(50) NOT NULL, 
    selected_team VARCHAR(255) NOT NULL,
    coefficient DECIMAL(5,2) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
