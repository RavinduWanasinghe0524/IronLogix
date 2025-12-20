@echo off
title BuildSmartOS - Quick Installer
color 0B

echo.
echo ================================================
echo     BuildSmartOS - Quick Installation
echo ================================================
echo.
echo This will install BuildSmartOS on your computer.
echo.
echo Installation includes:
echo   - Python package installation
echo   - Database setup
echo   - License initialization
echo   - Folder creation
echo.
echo Estimated time: 2-5 minutes
echo.
pause

REM Run Python installer
python install.py

REM Check if installation was successful
if errorlevel 1 (
    echo.
    echo ================================================
    echo   Installation Failed!
    echo ================================================
    echo.
    echo Please check the error messages above.
    echo.
    echo Common solutions:
    echo   1. Make sure Python 3.8+ is installed
    echo   2. Check your internet connection
    echo   3. Run as Administrator
    echo.
    echo Need help? Contact: 077-XXXXXXX
    echo.
    pause
    exit /b 1
)

echo.
echo ================================================
echo   Installation Successful!
echo ================================================
echo.
echo BuildSmartOS is ready to use.
echo.
echo Next Steps:
echo   1. Run: Run BuildSmartOS.bat
echo   2. Read: USER_MANUAL.md
echo.
pause
