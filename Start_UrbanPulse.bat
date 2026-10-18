@echo off
setlocal
cd /d "%~dp0"
title UrbanPulse Housing Intelligence

if exist "__pycache__" rmdir /s /q "__pycache__" >nul 2>&1
if exist "urbanpulse\__pycache__" rmdir /s /q "urbanpulse\__pycache__" >nul 2>&1

if not exist ".venv\Scripts\python.exe" (
    echo [1/3] Creating Python environment...
    py -m venv .venv
    if errorlevel 1 (echo Failed to create environment. Install Python 3.11+ and try again.&pause&exit /b 1)
)

if not exist ".venv\.urbanpulse_installed" (
    echo [2/3] Installing required packages...
    ".venv\Scripts\python.exe" -m pip install --upgrade pip
    ".venv\Scripts\python.exe" -m pip install -r requirements.txt
    if errorlevel 1 (echo Package installation failed.&pause&exit /b 1)
    type nul > ".venv\.urbanpulse_installed"
)

echo [3/3] Starting UrbanPulse...
start "" "http://127.0.0.1:5000"
".venv\Scripts\python.exe" app.py
pause
