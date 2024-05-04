CREATE TABLE expenses (
    id SERIAL PRIMARY KEY,
    date DATE,
    amount NUMERIC,
    category VARCHAR(255),
    notes TEXT
);
