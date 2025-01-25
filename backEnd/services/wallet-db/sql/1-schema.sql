
CREATE TABLE wallets (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL,
    balance DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
    currency VARCHAR(3) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    wallet_id INT NOT NULL REFERENCES wallets(id) ON DELETE CASCADE,
    amount DECIMAL(15, 2) NOT NULL,
    transaction_type VARCHAR(10) CHECK (transaction_type IN ('deposit', 'withdrawal')),
    status VARCHAR(20) CHECK (status IN ('pending', 'completed', 'failed')),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

