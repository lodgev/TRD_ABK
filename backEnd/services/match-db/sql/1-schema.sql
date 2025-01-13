CREATE TABLE clubs (
    id SERIAL PRIMARY KEY,
    rank INTEGER NOT NULL,
    club VARCHAR(255) NOT NULL,
    country VARCHAR(255) NOT NULL,
    level VARCHAR(50) NOT NULL,
    elo INTEGER NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL
);

CREATE TABLE matches (
    id SERIAL PRIMARY KEY,
    home_team_id INT REFERENCES clubs(id),
    away_team_id INT REFERENCES clubs(id),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL
);
