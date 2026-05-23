CREATE TABLE raw_jobs (
  id          SERIAL PRIMARY KEY,
  source      VARCHAR(50),
  job_title   TEXT,
  company     TEXT,
  location    TEXT,
  salary_min  NUMERIC,
  salary_max  NUMERIC,
  description TEXT,
  job_url     TEXT UNIQUE,
  posted_at   TIMESTAMP,
  fetched_at  TIMESTAMP DEFAULT NOW()
);