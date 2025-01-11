-- public.matchs definition
-- Drop table
-- DROP TABLE public.match;
CREATE TABLE public.match (
    id uuid NOT NULL,
    homeTeam varchar NOT NULL,
    homeScore int NOT NULL,
    awayTeam varchar NOT NULL,
    awayScore int NULL,
    scoreString varchar NULL,
    matchDate time NULL,
    CONSTRAINT matchs_pk PRIMARY KEY (id)
);