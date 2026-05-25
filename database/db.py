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

if __name__ == "__main__":
    try:
        conn = get_connection()
        print("Connected to PostgreSQL successfully!")
        conn.close()
    except Exception as e:
        print(f"Connection failed: {e}")