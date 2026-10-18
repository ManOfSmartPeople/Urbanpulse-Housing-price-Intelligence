@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    echo Please run Start_UrbanPulse.bat once first.
    pause
    exit /b 1
)
start "" http://127.0.0.1:5000
