# 📊 Trending SkillScope Dashboard

> A real-time UK job market intelligence tool that helps students and career switchers discover which technical skills employers demand most — built as a full end-to-end data engineering project.

**🔴 Live demo:** [skillscope-uk.streamlit.app](https://skillscope-uk.streamlit.app)

---

## Overview

SkillScope is a data engineering project that automatically collects, processes, and visualises UK job market data from [Reed.co.uk](https://reed.co.uk). It answers one core question for students preparing for the job market:

> *"I want to become a data engineer / ML engineer / DevOps engineer — what skills should I learn right now, and where are the opportunities?"*

The system runs a daily automated pipeline that fetches new job postings, extracts skill mentions from full job descriptions using regex keyword matching, and surfaces the results through an interactive Streamlit dashboard. The entire stack — from API ingestion to cloud deployment — mirrors patterns used in real data engineering teams.

---

## Project Scope

This project covers the full data engineering lifecycle:

- **Ingestion** — fetching live job postings from the Reed API with multi-page pagination and relevance filtering
- **Storage** — persisting raw and processed data in a cloud PostgreSQL database (Neon)
- **Transformation** — extracting 70+ technical skill mentions from full job descriptions using word-boundary regex
- **Orchestration** — automated daily pipeline runs via Windows Task Scheduler
- **Serving** — interactive dashboard deployed publicly on Streamlit Community Cloud

**Eight roles are tracked:**

| Role | Focus |
|---|---|
| Data Engineer | Pipelines, cloud, SQL, Spark |
| Data Analyst | SQL, BI tools, visualisation |
| Machine Learning Engineer | ML frameworks, MLOps, cloud |
| Data Scientist | Python, R, statistics, ML |
| Cloud Engineer | AWS, Azure, GCP, IaC |
| Software Engineer | Languages, CI/CD, architecture |
| DevOps Engineer | Kubernetes, Terraform, SRE |
| Cybersecurity Analyst | SIEM, incident response, compliance |

---

## Dataset Information

- **Source:** [Reed.co.uk Developer API](https://www.reed.co.uk/developers) (free tier)
- **Coverage:** UK-wide job postings, refreshed daily
- **Volume:** 700+ job postings across 8 roles (growing daily)
- **Fields collected:** job title, company, location, salary min/max, full description, posting date, job URL
- **Skill extraction:** 70+ skills across 7 categories (languages, data engineering tools, ML/AI, cloud, databases, BI & visualisation, DevOps & security)
- **Known limitation:** Reed's API returns a curated subset of live postings per search. Niche roles (cybersecurity analyst, cloud engineer) have smaller sample sizes than broad roles (software engineer, data analyst). This reflects the real UK job market volume on Reed, not a pipeline limitation.

---

## Project Architecture

Data flows through four distinct layers:

```
┌─────────────────────────────────────────────────────┐
│  INGESTION LAYER                                     │
│  Reed API → fetch.py → ingest.py                    │
│  Multi-page search · HTML stripping · deduplication  │
└───────────────────────┬─────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────┐
│  STORAGE LAYER — Neon Cloud PostgreSQL               │
│  raw_jobs table · skill_counts table                 │
└──────────┬────────────────────────┬─────────────────┘
           │                        │
┌──────────▼────────────────────────▼─────────────────┐
│  TRANSFORMATION LAYER                                │
│  extract_skills.py + skills_list.py                  │
│  Regex word-boundary matching · full refresh         │
└───────────────────────┬─────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────┐
│  SERVING LAYER — Streamlit Cloud                     │
│  data.py (SQL queries) → app.py (Plotly charts)      │
│  skillscope-uk.streamlit.app                         │
└─────────────────────────────────────────────────────┘
         ↑
  Windows Task Scheduler triggers daily at 09:00
```

**Key design decisions:**

- **Two-step Reed fetch** — search API returns job IDs; a second detail API call fetches the full description (~5,000 chars). This is what enables meaningful skill extraction, unlike single-call APIs that return 500-char truncated summaries.
- **Relevance filtering** — each role has a curated list of valid title keywords. Reed's fuzzy search returns broad results; the filter discards unrelated roles before the detail API is called, saving API quota and keeping data clean.
- **ON CONFLICT DO NOTHING** — jobs are uniquely identified by URL. Running the pipeline daily never creates duplicates.
- **Full refresh on skill_counts** — skill counts are deleted and rebuilt on every transformation run, ensuring the dashboard always reflects the current database state rather than accumulating stale rows.
- **Shared cloud database** — both developers point their local `.env` files at the same Neon PostgreSQL instance. Either machine can run the pipeline and results are immediately visible to both.

---

## Dashboard Features

The live dashboard at [skillscope-uk.streamlit.app](https://skillscope-uk.streamlit.app) has four sections, all updating instantly when a role is selected:

**Market snapshot** — four metric cards showing total jobs in database, top skill, average minimum salary, and average maximum salary for the selected role.

**Top skills** — horizontal bar chart of the top 10 skills by percentage of job postings. Uses percentages rather than raw counts so roles with different sample sizes remain comparable.

**Seniority breakdown** — bar chart classifying all job titles into Junior/Graduate, Mid-level, Senior/Lead, and Manager buckets. Includes a plain-English takeaway message telling students how competitive entry-level actually is for that role.

**Hot locations** — bar chart of UK cities with the most job postings. Postcodes and generic entries ("United Kingdom", "England") are filtered out using regex pattern matching, showing only named cities.

---

## Project Structure

```
Trending-SkillScope-Dashboard/
│
├── ingestion/
│   ├── fetch.py              # Reed API calls, HTML stripping, relevance filter
│   └── ingest.py             # Pipeline orchestration, DB insert, deduplication
│
├── transformation/
│   ├── extract_skills.py     # Regex skill extraction, skill_counts full refresh
│   └── skills_list.py        # 70+ skill keywords across 7 categories
│
├── database/
│   ├── db.py                 # psycopg2 + SQLAlchemy connection (local + cloud)
│   └── schema.sql            # CREATE TABLE statements for raw_jobs, skill_counts
│
├── dashboard/
│   ├── app.py                # Streamlit layout, Plotly charts, filtering logic
│   └── data.py               # SQL query functions returning pandas DataFrames
│
├── tests/                    # Placeholder for future unit tests
├── .env.example              # Template showing required environment variables
├── .gitignore
├── requirements.txt
├── run_pipeline.bat          # Windows one-click pipeline runner with logging
└── README.md
```

---

## Technologies Used

| Category | Technology | Purpose |
|---|---|---|
| Language | Python 3.11 | All pipeline and dashboard code |
| Data source | Reed.co.uk API | Live UK job postings |
| Database | PostgreSQL (Neon) | Cloud-hosted, shared between both developers |
| DB connector | psycopg2, SQLAlchemy | Python → PostgreSQL |
| Data processing | pandas | SQL → DataFrame → chart |
| HTML parsing | BeautifulSoup4 | Strip HTML from Reed descriptions |
| Text matching | re (regex) | Word-boundary skill extraction |
| Dashboard | Streamlit | Interactive web app framework |
| Charting | Plotly Express | Interactive bar charts |
| Deployment | Streamlit Community Cloud | Public hosting, free tier |
| Scheduling | Windows Task Scheduler | Daily 09:00 pipeline trigger |
| Version control | Git + GitHub | Collaborative development, two contributors |
| Environment | python-dotenv | Credential management |

---

## Local Setup

### Prerequisites

- Python 3.10+
- PostgreSQL (or a Neon free account)
- Reed Developer API key — [register free at reed.co.uk/developers](https://www.reed.co.uk/developers)
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/overseersnowfall/Trending-SkillScope-Dashboard.git
cd Trending-SkillScope-Dashboard

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # Mac / Linux
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt
```

### Environment configuration

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

```env
REED_API_KEY=your_reed_api_key_here
DB_HOST=your_neon_host_or_localhost
DB_NAME=job_market
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_PORT=5432
```

### Database setup

Run the schema in your PostgreSQL instance (or Neon SQL editor):

```bash
psql -U your_user -d job_market -f database/schema.sql
```

### Running the pipeline

```bash
# Test database connection
python database/db.py

# Run ingestion (fetches jobs from Reed API)
python ingestion/ingest.py

# Run skill extraction (populates skill_counts table)
python transformation/extract_skills.py

# Launch the dashboard
streamlit run dashboard/app.py
```

The dashboard will open at `http://localhost:8501`.

---

## Future Improvements

- **Apache Airflow** — replace the Windows Task Scheduler bat file with a proper DAG-based orchestration system with retries, alerting, and dependency management
- **dbt (data build tool)** — replace the pandas transformation scripts with versioned, tested SQL models following modern analytics engineering practices
- **Second data source** — add LinkedIn or Adzuna alongside Reed to increase coverage and enable source comparison
- **Historical trend charts** — surface how skill demand changes week-over-week using the `fetched_at` timestamps already stored in `raw_jobs`
- **Unit tests** — add pytest coverage for the skill extraction logic and data query functions
- **Docker** — containerise the pipeline so it runs identically on any machine without environment setup
- **Salary trend analysis** — track how average salaries for each role change over time as the database grows

---

## Contributors

Built by two first-year Computer Science students at university as a practical data engineering project, using a real-world tool stack to explore ingestion, transformation, storage, and serving patterns.

- [@overseersnowfall](https://github.com/overseersnowfall)
- [@larry](https://github.com/larry)

---

## Licence

MIT — see [LICENSE](LICENSE) for details.