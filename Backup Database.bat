@echo off
echo ============================================================
echo BuildSmartOS - Database Backup
echo ============================================================
echo.
echo Creating database backup...
echo.

python database_setup.py

echo.
echo Backup complete! Check the backups/ folder.
echo.
pause
