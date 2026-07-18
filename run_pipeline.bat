REM comment Windows to run it automatically without setting up full Task Scheduler yet

@echo off
call venv\Scripts\activate
python ingestion/ingest.py
python transformation/extract_skills.py
echo Pipeline complete.