import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def _get_db_config():
    """
    Get database credentials.
    Uses Streamlit secrets when deployed, .env for local development.
    """
    try:
        import streamlit as st
        return {
            "host"    : st.secrets["DB_HOST"],
            "dbname"  : st.secrets["DB_NAME"],
            "user"    : st.secrets["DB_USER"],
            "password": st.secrets["DB_PASSWORD"],
            "port"    : st.secrets.get("DB_PORT", "5432")
        }
    except Exception:
        return {
            "host"    : os.getenv("DB_HOST"),
            "dbname"  : os.getenv("DB_NAME"),
            "user"    : os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "port"    : os.getenv("DB_PORT", "5432")
        }

def get_connection():
    """Return a live psycopg2 connection to the job_market database."""
    config = _get_db_config()
    return psycopg2.connect(**config, sslmode="require")

from sqlalchemy import create_engine

def get_engine():
    """Return a SQLAlchemy engine for use with pandas read_sql."""
    config = _get_db_config()
    db_url = (
        f"postgresql+psycopg2://"
        f"{config['user']}:{config['password']}"
        f"@{config['host']}:{config['port']}"
        f"/{config['dbname']}"
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