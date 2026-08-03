@echo off
cd /d C:\Users\User\Trending-SkillScope-Dashboard

set LOG=logs\pipeline.log

echo =================================== >> %LOG%
echo %date% %time% >> %LOG%
echo =================================== >> %LOG%

venv\Scripts\python.exe ingestion\ingest.py >> %LOG% 2>&1
venv\Scripts\python.exe transformation\extract_skills.py >> %LOG% 2>&1

echo Pipeline complete: %time% >> %LOG%
echo. >> %LOG%