import sys
import os

# Add the project root to Python's path so it can find the database folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fetch import fetch_jobs
from database.db import get_connection

ROLES = [
    "data engineer",
    "data analyst",
    "machine learning engineer",
    "data scientist",
    "cloud engineer",
    "software engineer",
    "devops engineer",
    "cybersecurity analyst"
]

def insert_jobs(conn, jobs):
    """Insert a list of job dicts into raw_jobs. Skips duplicates."""
    cursor = conn.cursor()
    inserted = 0

    sql = """
        INSERT INTO raw_jobs (
            source, job_title, company, location,
            salary_min, salary_max, description,
            job_url, posted_at
        ) VALUES (
            %(search_term)s, %(job_title)s, %(company)s, %(location)s,
            %(salary_min)s, %(salary_max)s, %(description)s,
            %(job_url)s, %(posted_at)s
        ) ON CONFLICT (job_url) DO NOTHING
    """ 

    for job in jobs:
        if not job.get("job_url"):
            continue
        cursor.execute(sql, job)
        if cursor.rowcount == 1:
            inserted += 1
    conn.commit()
    cursor.close()
    return inserted

def run_pipeline():
    """Run the full ingestion pipeline for all roles."""
    try:
        conn = get_connection()
    except Exception as e:
        print(f"Could not connect to database: {e}")
        sys.exit(1)

    total_inserted = 0
    for role in ROLES:
        print(f"Fetching: {role}...")
        jobs = fetch_jobs(role)
        print(f"  Got {len(jobs)} jobs from API")
        inserted = insert_jobs(conn, jobs)
        print(f"  Inserted {inserted} new rows (duplicates skipped)")
        total_inserted += inserted
    conn.close()
    print(f"\nDone. Total new jobs inserted: {total_inserted}")

if __name__ == "__main__":
    run_pipeline()