@echo off
cd /d C:\Users\User\Trending-SkillScope-Dashboard
call venv\Scripts\activate

echo =================================== >> logs\pipeline.log
echo %date% %time% >> logs\pipeline.log
echo =================================== >> logs\pipeline.log

python ingestion\ingest.py >> logs\pipeline.log 2>&1
python transformation\extract_skills.py >> logs\pipeline.log 2>&1

echo Pipeline complete %time% >> logs\pipeline.log
echo. >> logs\pipeline.log