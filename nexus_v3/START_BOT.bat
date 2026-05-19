@echo off
title NEXUS AI TRADER v3.0
color 0A
echo.
echo  ================================================
echo   NEXUS AI TRADER v3.0
echo   "Any profit is good — even 0.1 percent"
echo  ================================================
echo.
cd /d "%~dp0"
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
) else (
    echo Creating virtual environment...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    python setup.py
)
echo Starting NEXUS Agent...
echo Press Ctrl+C to stop safely.
echo.
python bot.py
echo.
echo Bot stopped safely.
pause