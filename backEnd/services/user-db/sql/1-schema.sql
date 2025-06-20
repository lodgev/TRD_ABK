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

