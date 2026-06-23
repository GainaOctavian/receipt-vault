import os
import psycopg

# Connection string built from environment variables
DB_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://receipts:receipts@localhost:5432/receipts",
)


def get_connection():
    """Open a new connection to Postgres."""
    return psycopg.connect(DB_URL)


# Schema kept in code so the worker can ensure it exists at startup
SCHEMA = """
CREATE TABLE IF NOT EXISTS receipts (
    id           SERIAL PRIMARY KEY,
    s3_key       TEXT NOT NULL,
    vendor       TEXT,
    amount       NUMERIC(10, 2),
    receipt_date DATE,
    created_at   TIMESTAMPTZ DEFAULT now()
);
"""


def ensure_schema():
    """Create the receipts table if it does not exist yet."""
    with get_connection() as conn:
        conn.execute(SCHEMA)
        conn.commit()