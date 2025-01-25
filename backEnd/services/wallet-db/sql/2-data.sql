INSERT INTO wallets (user_id, balance, currency)
VALUES (        'f928c455-d2f3-4e30-bf58-178ae041e8c2'::uuid, 1000.00, 'USD');

INSERT INTO transactions (wallet_id, amount, transaction_type, status)
VALUES (1, 200.00, 'deposit', 'completed');
