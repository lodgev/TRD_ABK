CREATE TABLE clubs (
    id SERIAL PRIMARY KEY,
    rank INTEGER NOT NULL,
    club VARCHAR(255) NOT NULL,
    country VARCHAR(255) NOT NULL,
    level VARCHAR(50) NOT NULL,
    elo INTEGER NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    likes INTEGER
);

CREATE TABLE matches (
    match_id BIGINT PRIMARY KEY,
    home_team VARCHAR(255) NOT NULL,
    home_score INT NOT NULL,
    away_team VARCHAR(255) NOT NULL,
    away_score INT NOT NULL,
    score_string VARCHAR(20),
    match_date TIMESTAMP NOT NULL,
    home_coeff FLOAT NOT NULL, 
    away_coeff FLOAT NOT NULL
);

CREATE TABLE odds (
    match_id BIGINT PRIMARY KEY,
    home_win FLOAT NOT NULL,
    draw FLOAT NOT NULL,
    away_win FLOAT NOT NULL
);


