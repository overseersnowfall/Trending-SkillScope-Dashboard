import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.adzuna.com/v1/api/jobs/gb/search/1"
APP_ID  = os.getenv("ADZUNA_APP_ID")
API_KEY = os.getenv("ADZUNA_API_KEY")

def fetch_jobs(role, results_per_page=50):
    """
    Fetch job postings from Adzuna for a given role.
    Returns a list of job dictionaries.
    """
    params = {
        "app_id"          : APP_ID,
        "app_key"         : API_KEY,
        "what"            : role,
        "results_per_page": results_per_page,
        "content-type"    : "application/json"
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    
        jobs = []
        for job in data.get("results", []):
            jobs.append({
                "job_title"  : job.get("title"),
                "company"    : job.get("company", {}).get("display_name"),
                "location"   : job.get("location", {}).get("display_name"),
                "salary_min" : job.get("salary_min"),
                "salary_max" : job.get("salary_max"),
                "description": job.get("description"),
                "job_url"    : job.get("redirect_url"),
                "posted_at"  : job.get("created"),
                "search_term": role
            })
        return jobs

    except requests.exceptions.RequestException as e:
        print(f"API request failed for role '{role}': {e}")
        return []

if __name__ == "__main__":
    jobs = fetch_jobs("data engineer")
    print(f"Fetched {len(jobs)} jobs")
    for job in jobs[:3]:
        print(job["job_title"], "|", job["company"], "|", job["location"])