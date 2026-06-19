-- Table that stores the extracted receipt metadata
CREATE TABLE IF NOT EXISTS receipts (
    id          SERIAL PRIMARY KEY,
    s3_key      TEXT NOT NULL,        -- where the raw file lives in S3
    vendor      TEXT,                 -- extracted vendor name
    amount      NUMERIC(10, 2),       -- extracted total amount
    receipt_date DATE,                -- extracted date
    created_at  TIMESTAMPTZ DEFAULT now()
);