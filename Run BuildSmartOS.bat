@echo off
cd /d "%~dp0"
title BuildSmartOS - Hardware POS System

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Check if first-run configuration is needed
if not exist ".configured" (
    echo First-time setup detected...
    echo Running configuration wizard...
    python first_run_wizard.py
)

REM Run startup checks and launch application
echo Running system checks...
python startup.py

REM If startup script fails, try direct launch
if errorlevel 1 (
    echo.
    echo Startup checks failed, trying direct launch...
    python main.pyw
    
    if errorlevel 1 (
        python main.py
    )
)

pause
