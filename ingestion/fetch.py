import os
import requests
from dotenv import load_dotenv

load_dotenv()


"""
first attempt at fetching jobs from adzuna API but it has 100 character limit on job description
BASE_URL = "https://api.adzuna.com/v1/api/jobs/gb/search/1"
APP_ID  = os.getenv("ADZUNA_APP_ID")
API_KEY = os.getenv("ADZUNA_API_KEY")

def fetch_jobs(role, results_per_page=50):
    ""(comment here)
    Fetch job postings from Adzuna for a given role.
    Returns a list of job dictionaries.
    ""
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

"""
#trying reed API instead, which has no character limit on job description

REED_API_KEY = os.getenv("REED_API_KEY")
SEARCH_URL   = "https://www.reed.co.uk/api/1.0/search"
DETAILS_URL  = "https://www.reed.co.uk/api/1.0/jobs/{job_id}"

# Keywords that must appear in the job title for each role
ROLE_TITLE_KEYWORDS = {
    "data engineer"              : ["data engineer", "data engineering"],
    "data analyst"               : ["data analyst", "data analysis"],
    "machine learning engineer"  : ["machine learning", "ml engineer"],
    "data scientist"             : ["data scientist", "data science"],
    "cloud engineer"             : ["cloud engineer", "cloud architect",
                                    "cloud platform", "platform engineer"],
    "software engineer"          : ["software engineer", "software developer",
                                    "software development"],
    "devops engineer"            : ["devops", "dev ops", "site reliability",
                                    "sre", "platform engineer"],
    "cybersecurity analyst"      : ["cyber", "security analyst",
                                    "information security", "infosec",
                                    "penetration", "soc analyst"]
}

def is_relevant_job(job_title, role):
    """
    Return True if the job title is genuinely relevant to the searched role.
    Prevents Reed's fuzzy search from polluting our data with unrelated jobs.
    """
    if not job_title:
        return False
    title_lower = job_title.lower()
    keywords = ROLE_TITLE_KEYWORDS.get(role, [])
    return any(keyword in title_lower for keyword in keywords)

def convert_date(date_str):
    """Convert Reed's DD/MM/YYYY date format to YYYY-MM-DD for PostgreSQL."""
    if not date_str:
        return None
    try:
        day, month, year = date_str.split("/")
        return f"{year}-{month}-{day}"
    except:
        return None

def fetch_job_details(job_id):
    """
    Fetch the full description for one job using its ID.
    Returns the description string or None if it fails.
    """
    url = DETAILS_URL.format(job_id=job_id)
    try:
        response = requests.get(
            url,
            auth=(REED_API_KEY, ""),
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        return data.get("jobDescription")
    except requests.exceptions.RequestException:
        return None

def fetch_jobs(role, results_per_page=50):
    """
    Fetch job postings from Reed for a given role.
    Step 1: search for jobs to get IDs and basic info.
    Step 2: fetch full description for each job individually.
    Returns a list of job dictionaries.
    """
    params = {
        "keywords"      : role,
        "locationName"  : "UK",
        "resultsToTake" : results_per_page,
        "resultsToSkip" : 0
    }

    try:
        response = requests.get(
            SEARCH_URL,
            params=params,
            auth=(REED_API_KEY, ""),
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"  Search failed for '{role}': {e}")
        return []

    jobs = []
    results = data.get("results", [])
    print(f"  Fetching full descriptions for {len(results)} jobs...")

    for job in results:
        job_title = job.get("jobTitle", "")

        # Skip jobs that aren't relevant to the searched role
        if not is_relevant_job(job_title, role):
            continue

        job_id      = job.get("jobId")
        description = fetch_job_details(job_id) if job_id else None

        jobs.append({
            "job_title"  : job_title,
            "company"    : job.get("employerName"),
            "location"   : job.get("locationName"),
            "salary_min" : job.get("minimumSalary"),
            "salary_max" : job.get("maximumSalary"),
            "description": description,
            "job_url"    : job.get("jobUrl"),
            "posted_at"  : convert_date(job.get("date")),
            "search_term": role
        })

    return jobs


if __name__ == "__main__":
    jobs = fetch_jobs("data engineer", results_per_page=3)
    print(f"\nFetched {len(jobs)} jobs")
    for job in jobs:
        desc_len = len(job["description"]) if job["description"] else 0
        print(f"{job['job_title']} | {job['company']} | desc: {desc_len} chars")