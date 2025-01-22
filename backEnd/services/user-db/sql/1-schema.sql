-- public.users definition
-- Drop table
-- DROP TABLE public.users;
CREATE TABLE public.users (
    id uuid NOT NULL,
    email varchar NOT NULL,
    "password" varchar NOT NULL,
    refreshtoken varchar NULL,
    createdat time NOT NULL,
    updatedat time NULL,
    lastsigninat time NULL,
    firstname varchar NOT NULL,
    lastname varchar NOT NULL,
    is_verified boolean NOT NULL,
    reset_token varchar NULL,
    reset_token_expiration time NULL,
    CONSTRAINT users_pk PRIMARY KEY (id),
    CONSTRAINT users_unique UNIQUE (email)
);

CREATE TABLE user_stats (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    club_id INTEGER NOT NULL REFERENCES clubs(id) ON DELETE CASCADE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, club_id) -- Користувач може лайкнути клуб тільки один раз
);
