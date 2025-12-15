@echo off
cd /d "%~dp0"
@echo off
REM BuildSmartOS Launcher with First-Run Detection

REM Check if first-run configuration is needed
if not exist ".configured" (
    echo First-time setup detected...
    echo Running configuration wizard...
    python first_run_wizard.py
)

REM Launch main application
python main.py
pause
