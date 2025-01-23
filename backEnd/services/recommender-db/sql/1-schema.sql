-- -- Create the football_transfers table
-- CREATE TABLE IF NOT EXISTS football_transfers (
--     id SERIAL PRIMARY KEY,
--     name VARCHAR(100),
--     player_id INTEGER,
--     position VARCHAR(50),
--     transfer_date TIMESTAMP,
--     from_club VARCHAR(100),
--     from_club_id INTEGER,
--     to_club VARCHAR(100),
--     to_club_id INTEGER,
--     fee_value NUMERIC,
--     transfer_type VARCHAR(50),
--     contract_extension BOOLEAN,
--     on_loan BOOLEAN,
--     market_value NUMERIC
-- );

CREATE TABLE IF NOT EXISTS user_actions (
    click_id SERIAL PRIMARY KEY,
    club_id INTEGER NOT NULL,
    user_id UUID NOT NULL,
    action VARCHAR(50) NOT NULL CHECK (action IN ('liked', 'disliked', 'commented')),
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


