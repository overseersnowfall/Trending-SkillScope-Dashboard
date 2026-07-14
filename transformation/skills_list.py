SKILLS = {
    "languages": [
        "python", "sql", "java", "scala", "r", "javascript",
        "typescript", "go", "golang", "bash", "powershell",
        "c#", "ruby", "rust", "php", "t-sql", "pl/sql"
    ],
    "data_tools": [
        "pandas", "spark", "airflow", "dbt", "kafka",
        "hadoop", "snowflake", "databricks", "power bi",
        "powerbi", "tableau", "looker", "ssis", "ssrs",
        "dask", "flink", "hive", "nifi", "prefect", "luigi"
    ],
    "cloud": [
        "aws", "azure", "gcp", "google cloud",
        "terraform", "kubernetes", "docker",
        "cloudformation", "ansible", "pulumi",
        "lambda", "ec2", "s3", "azure devops",
        "google kubernetes engine", "eks", "aks"
    ],
    "databases": [
        "postgresql", "postgres", "mysql", "mongodb",
        "redis", "oracle", "nosql", "bigquery", "redshift",
        "synapse", "sql server", "cassandra", "dynamodb",
        "elasticsearch", "neo4j", "mariadb", "sqlite"
    ],
    "ml_ai": [
        "machine learning", "ml", "mlops", "tensorflow", "pytorch",
        "scikit-learn", "nlp", "deep learning", "llm",
        "generative ai", "computer vision", "hugging face",
        "xgboost", "keras", "langchain", "openai",
        "feature engineering", "model deployment"
    ],
    "devops_practices": [
        "git", "ci/cd", "agile", "etl", "elt",
        "api", "rest", "microservices", "devops", "scrum",
        "jenkins", "github actions", "gitlab ci", "circleci",
        "helm", "prometheus", "grafana", "datadog",
        "linux", "nginx", "observability", "sre"
    ],
    "cybersecurity": [
        "siem", "soc", "penetration testing", "pen testing",
        "vulnerability assessment", "firewalls", "ids", "ips",
        "zero trust", "iam", "oauth", "encryption",
        "gdpr", "iso 27001", "nist",
        "threat intelligence", "incident response",
        "ethical hacking", "network security", "endpoint security",
        "splunk", "wireshark", "burp suite", "owasp"
    ]
}


def get_all_skills():
    """Flatten the category dict into one list of all skill keywords."""
    all_skills = []
    for category, skills in SKILLS.items():
        all_skills.extend(skills)
    return all_skills