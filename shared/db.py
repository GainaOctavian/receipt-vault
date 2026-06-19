import os
import psycopg

DB_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://receipts:receipts@localhost:5432/receipts",
)


def get_connection():
    """Open a new connection to Postgres."""
    return psycopg.connect(DB_URL)