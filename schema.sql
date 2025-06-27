CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20),
    side VARCHAR(10),
    status VARCHAR(20),
    entry_price NUMERIC,
    stop_loss NUMERIC,
    take_profit NUMERIC,
    indicators JSONB,
    created_at TIMESTAMP,
    closed_at TIMESTAMP
);

CREATE TABLE trades (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id),
    price NUMERIC,
    quantity NUMERIC,
    created_at TIMESTAMP
);

CREATE TABLE positions (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20),
    side VARCHAR(10),
    quantity NUMERIC,
    entry_price NUMERIC,
    stop_loss NUMERIC,
    take_profit NUMERIC,
    created_at TIMESTAMP
);

CREATE TABLE logs (
    id SERIAL PRIMARY KEY,
    level VARCHAR(10),
    message TEXT,
    created_at TIMESTAMP
);
