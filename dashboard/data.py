import sys, os
import pandas as pd
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db import get_engine


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

def get_seniority_breakdown(role):
    """
    Classify job titles by seniority level and return percentage breakdown.
    Uses job_title text from raw_jobs — no extra API calls needed.
    """
    engine = get_engine()

    sql = """
        SELECT job_title
        FROM raw_jobs
        WHERE source = %s
        AND job_title IS NOT NULL
    """
    df = pd.read_sql(sql, engine, params=(role,))

    if df.empty:
        return pd.DataFrame()

    # Classify each title into a seniority bucket
    def classify(title):
        t = title.lower()
        if any(w in t for w in [
            "junior", "jr", "graduate", "grad",
            "entry", "trainee", "apprentice", "associate"
        ]):
            return "Junior / Graduate"
        elif any(w in t for w in [
            "senior", "sr", "principal", "staff",
            "lead", "head", "director", "vp", "chief"
        ]):
            return "Senior / Lead"
        elif any(w in t for w in [
            "manager", "managing", "management"
        ]):
            return "Manager"
        else:
            return "Mid-level"

    df["seniority"] = df["job_title"].apply(classify)

    total = len(df)
    breakdown = (
        df["seniority"]
        .value_counts()
        .reset_index()
    )
    breakdown.columns = ["seniority", "count"]
    breakdown["percentage"] = (
        breakdown["count"] / total * 100
    ).round(1)

    # Fix ordering so chart reads Junior → Mid → Senior → Manager
    order = ["Junior / Graduate", "Mid-level", "Senior / Lead", "Manager"]
    breakdown["seniority"] = pd.Categorical(
        breakdown["seniority"], categories=order, ordered=True
    )
    breakdown = breakdown.sort_values("seniority")

    return breakdown, total

def get_top_skills(role, limit=10):
    """Return a DataFrame of top skills with counts and percentages."""
    engine = get_engine()
    
    # Get total jobs for this role to calculate percentage
    total_sql = "SELECT COUNT(*) as total FROM raw_jobs WHERE source = %s"
    total_df  = pd.read_sql(total_sql, engine, params=(role,))
    total     = int(total_df["total"][0])

    sql = """
        SELECT skill, count,
               ROUND((count::float / %s * 100)::numeric, 1) AS percentage
        FROM skill_counts
        WHERE role = %s
        ORDER BY count DESC
        LIMIT %s
    """
    df = pd.read_sql(sql, engine, params=(total, role, limit))
    return df, total

def get_salary_summary(role):
    """Return avg min and avg max salary for a role."""
    engine = get_engine()
    sql = """
        SELECT
            ROUND(AVG(salary_min)) AS avg_min,
            ROUND(AVG(salary_max)) AS avg_max,
            COUNT(*) AS total_jobs
        FROM raw_jobs
        WHERE source = %s
        AND salary_min IS NOT NULL
    """
    df = pd.read_sql(sql, engine, params=(role,))
    return df

def get_total_jobs(role):
    """Return total number of jobs stored for a role."""
    engine = get_engine()
    sql = "SELECT COUNT(*) AS total FROM raw_jobs WHERE source = %s"
    df = pd.read_sql(sql, engine, params=(role,))
    return int(df["total"][0])

def get_top_locations(role, limit=10):
    """Return top UK locations by job count for a role."""
    engine = get_engine()
    sql = """
        SELECT location, COUNT(*) AS job_count
        FROM raw_jobs
        WHERE source = %s
        AND location IS NOT NULL
        GROUP BY location
        ORDER BY job_count DESC
        LIMIT %s
    """
    df = pd.read_sql(sql, engine, params=(role, limit))
    return df

def get_comparison_skills(role1, role2, limit=10):
    """
    Return skills that appear in both roles for comparison.
    Returns a single DataFrame with columns: skill, role1_count, role2_count
    """
    engine = get_engine()
    sql = """
        SELECT
            a.skill,
            a.count AS role1_count,
            b.count AS role2_count
        FROM skill_counts a
        JOIN skill_counts b ON a.skill = b.skill
        WHERE a.role = %s
        AND b.role = %s
        ORDER BY (a.count + b.count) DESC
        LIMIT %s
    """
    df = pd.read_sql(sql, engine, params=(role1, role2, limit))
    return df

if __name__ == "__main__":
    print(get_top_skills("data engineer"))
    print(get_salary_summary("data engineer"))
    print(get_total_jobs("data engineer"))
    print(get_top_locations("data engineer"))
    print(get_comparison_skills("data engineer", "data analyst"))