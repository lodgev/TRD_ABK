INSERT INTO public.users (
        id,
        email,
        "password",
        refreshtoken,
        createdat,
        updatedat,
        lastsigninat,
        firstname,
        lastname
    )
VALUES (
        'f928c455-d2f3-4e30-bf58-178ae041e8c2'::uuid,
        'john@doe.com',
        'pbkdf2:sha256:600000$KBWNCEgW$cd3de4f2b261be199a8ecec6beb0931aa5ccfa264afbb526386a8960fa44bf02',
        NULL,
        '19:08:26.746',
        NULL,
        NULL,
        'John',
        'Doe'
    );