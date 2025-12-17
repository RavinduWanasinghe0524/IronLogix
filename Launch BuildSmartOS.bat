@echo off
REM ===================================================
REM BuildSmartOS - One-Click Launcher
REM ===================================================

echo.
echo ========================================
echo   BuildSmartOS - Hardware POS System
echo   Made in Sri Lanka with Love
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo Please install Python 3.8 or later from python.org
    pause
    exit /b 1
)

REM Check if database exists
if not exist "buildsmart_hardware.db" (
    echo First time setup detected...
    echo Running database initialization...
    python database_setup.py
    echo.
)

REM Check if configured
if not exist ".configured" (
    echo Starting first-run setup wizard...
    python first_run_wizard.py
    echo.
)

REM Launch application
echo Starting BuildSmartOS...
echo.
python main.py

if errorlevel 1 (
    echo.
    echo ERROR: Application failed to start
    echo Check the logs folder for details
    pause
)
