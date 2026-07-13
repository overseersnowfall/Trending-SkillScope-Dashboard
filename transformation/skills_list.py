SKILLS = {
    "languages": [
        "python", "sql", "java", "scala", "r", "javascript",
        "python3", "t-sql", "pl/sql"
    ],
    "data_tools": [
        "pandas", "spark", "airflow",
        "dbt", "kafka", "hadoop", "snowflake", "databricks",
        "power bi", "powerbi", "tableau", "looker", "ssis", "ssrs"
    ],
    "cloud": [
        "aws", "azure", "gcp", "google cloud",
        "terraform", "kubernetes", "docker"
    ],
    "databases": [
        "postgresql", "postgres", "mysql", "mongodb",
        "redis", "oracle", "nosql", "bigquery", "redshift",
        "synapse", "sql server"
    ],
    "ml_ai": [
        "machine learning", "ml", "mlops", "tensorflow", "pytorch",
        "scikit-learn", "nlp", "deep learning", "llm", "generative ai",
        "computer vision"
    ],
    "practices": [
        "git", "ci/cd", "agile", "etl", "elt",
        "api", "rest", "microservices", "devops", "scrum"
    ]
}


def get_all_skills():
    """Flatten the category dict into one list of all skill keywords."""
    all_skills = []
    for category, skills in SKILLS.items():
        all_skills.extend(skills)
    return all_skills