# 🚀 BuildSmartOS - Quick Reference

## Start Application
```bash
# Windows - Double click this file
Run BuildSmartOS.bat

# Or run directly
python startup.py

# Or minimal start (skip checks)
python main.py
```

## Essential Commands

### Health Check
```bash
python health_monitor.py
```

### Create Backup
```bash
python -c "from backup_manager import create_backup; create_backup()"
```

### List Backups
```bash
python -c "from backup_manager import list_backups; [print(f\"{b['date']}: {b['filename']}\") for b in list_backups()]"
```

### Restore Backup
```python
from backup_manager import restore_backup
restore_backup("backups/buildsmart_backup_YYYYMMDD_HHMMSS.db")
```

### Check Database
```bash
python database_setup.py
```

### Install Dependencies
```bash
# All dependencies (recommended)
pip install -r requirements.txt

# Core only (minimal)
pip install customtkinter pillow reportlab

# Add optional features
pip install psutil schedule  # System monitoring & auto-backup
pip install matplotlib pandas  # Analytics
pip install pywhatkit  # WhatsApp
pip install opencv-python pyzbar  # Barcode scanner
pip install SpeechRecognition pyttsx3  # Voice commands
```

## Configuration

### Setup Environment
```bash
# Create .env from template
copy .env.example .env

# Edit with your details
notepad .env
```

### Key Settings in config.json
```json
{
  "business": {
    "name": "Your Store Name",
    "phone": "077-1234567"
  },
  "features": {
    "whatsapp_enabled": true,
    "loyalty_enabled": true
  }
}
```

## Common Tasks

### Add Products
1. Click **📦 Products** button
2. Click "Add New Product"
3. Fill in details and save

### Process Sale
1. Click products to add to cart
2. Click "Add Customer" (optional)
3. Check "Send WhatsApp" if desired
4. Click "Checkout"

### Generate Reports
1. Click **📄 Reports** button
2. Select date range
3. Choose report type
4. Click "Generate"

### Process Refund
1. Click **🔄 Refunds** button
2. Search by phone or transaction ID
3. Select transaction
4. Process refund

### View Analytics
1. Click **📊 Analytics** button
2. View sales summary
3. Check top products
4. Review trends

## File Locations

- **Database:** `buildsmart_hardware.db`
- **Backups:** `backups/` folder
- **Invoices:** `bills/` folder
- **Reports:** `reports/` folder
- **Logs:** `logs/` folder
- **Config:** `config.json`

## Keyboard Shortcuts (in app)

- **Ctrl+F** - Focus search
- **Ctrl+N** - New transaction
- **Ctrl+P** - Products manager
- **Ctrl+R** - Reports
- **Ctrl+B** - Backup now
- **F5** - Refresh products
- **Esc** - Clear cart

## Troubleshooting Quick Fixes

### App Won't Start
```bash
# Check dependencies
pip install -r requirements.txt

# Check database
python database_setup.py

# Run health check
python health_monitor.py
```

### Database Errors
```bash
# Fix database
python fix_database.py

# Or restore backup
python -c "from backup_manager import list_backups, restore_backup; restore_backup(list_backups()[0]['filepath'])"
```

### Missing Features
```bash
# Install optional dependencies
pip install psutil schedule matplotlib pandas
```

### Configuration Issues
```bash
# Reset to defaults
python -c "from config_manager import get_config_manager; get_config_manager().reset_to_defaults()"
```

## Daily Checklist

- [ ] Check low stock alerts (shown on startup)
- [ ] Review today's sales
- [ ] Process any pending refunds
- [ ] Respond to customer inquiries

## Weekly Checklist

- [ ] Run health check: `python health_monitor.py`
- [ ] Review weekly sales report
- [ ] Update product prices if needed
- [ ] Clean up old invoices/reports

## Monthly Checklist

- [ ] Generate monthly report
- [ ] Review backup count (should have 30+)
- [ ] Update dependencies: `pip install -r requirements.txt --upgrade`
- [ ] Archive old data if needed

## Emergency Procedures

### Database Corrupted
```bash
# 1. List backups
python -c "from backup_manager import list_backups; [print(f\"{i}: {b['date']} - {b['filename']}\") for i, b in enumerate(list_backups())]"

# 2. Restore most recent
python -c "from backup_manager import restore_backup, list_backups; restore_backup(list_backups()[0]['filepath'])"
```

### App Crashes
1. Check `logs/error_log.txt` for errors
2. Run `python health_monitor.py`
3. Try restarting with `python main.py`

### Lost Data
1. Check `backups/` folder
2. Use most recent backup
3. Run `python backup_manager.py` to restore

## Support Files

- **User Guide:** `USER_MANUAL.md`
- **Installation:** `INSTALLATION_GUIDE.md`
- **Troubleshooting:** `TROUBLESHOOTING.md`
- **Changes:** `FIXES_AND_ENHANCEMENTS.md`
- **Summary:** `SUMMARY.md`

## Version Info

- **Version:** 1.0 (Stable)
- **Last Updated:** December 15, 2024
- **Python Required:** 3.8+
- **Platform:** Windows/Linux/macOS

## Quick Stats

Check system status anytime:
```python
from health_monitor import get_health_monitor
stats = get_health_monitor().get_system_stats()
print(stats)
```

---

**Need Help?** Run `python health_monitor.py` for diagnostics!

**Keep This File Handy for Quick Reference!** 📌
