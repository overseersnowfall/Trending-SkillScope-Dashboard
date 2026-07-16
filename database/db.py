import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    """Return a live psycopg2 connection to the job_market database."""
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT", "5432"),
        sslmode="require"
    )

from sqlalchemy import create_engine

def get_engine():
    """Return a SQLAlchemy engine for use with pandas read_sql."""
    load_dotenv()
    db_url = (
        f"postgresql+psycopg2://"
        f"{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT', '5432')}"
        f"/{os.getenv('DB_NAME')}"
        f"?sslmode=require"
    )
    return create_engine(db_url)

if __name__ == "__main__":
    try:
        conn = get_connection()
        print("Connected to PostgreSQL successfully!")
        conn.close()
    except Exception as e:
        print(f"Connection failed: {e}")