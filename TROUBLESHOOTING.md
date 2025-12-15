# BuildSmartOS Troubleshooting Guide

**Quick Problem Resolution**

---

## Table of Contents

1. [Installation Issues](#installation-issues)
2. [Application Launch Problems](#application-launch-problems)
3. [Database Issues](#database-issues)
4. [Feature-Specific Issues](#feature-specific-issues)
5. [Performance Problems](#performance-problems)
6. [Integration Issues](#integration-issues)
7. [Common Error Messages](#common-error-messages)

---

## Installation Issues

### Problem: pip install fails with "No module named pip"

**Symptoms:**
- Error when running `pip install -r requirements.txt`
- Message: "'pip' is not recognized as an internal or external command"

**Solutions:**

1. **Reinstall pip:**
   ```bash
   python -m ensurepip --upgrade
   ```

2. **Use python -m pip:**
   ```bash
   python -m pip install -r requirements.txt
   ```

3. **Verify Python installation:**
   ```bash
   python --version
   # Should show Python 3.8 or higher
   ```

### Problem: Dependency installation is very slow

**Symptoms:**
- Packages taking 10+ minutes to install
- "Downloading..." messages hanging

**Solutions:**

1. **Use --no-cache-dir:**
   ```bash
   pip install -r requirements.txt --no-cache-dir
   ```

2. **Install critical packages only:**
   ```bash
   pip install customtkinter reportlab matplotlib pandas numpy qrcode
   ```

3. **Skip optional packages:**
   - opencv-python (large, for barcode only)
   - scikit-learn (large, for AI only)
   - Install these later if needed

### Problem: "Microsoft Visual C++ 14.0 is required"

**Symptoms:**
- Error during package installation
- Mentions C++ build tools

**Solution:**

1. **Download Visual C++ Redistributable:**
   - Visit: https://visualstudio.microsoft.com/downloads/
   - Download "Build Tools for Visual Studio"
   - Install C++ build tools

2. **Alternative - Use precompiled wheels:**
   ```bash
   pip install --only-binary :all: package_name
   ```

### Problem: Permission denied when installing packages

**Symptoms:**
- "Access is denied" error
- Permission errors during installation

**Solutions:**

1. **Run as Administrator:**
   - Right-click Command Prompt
   - Select "Run as Administrator"
   - Try installation again

2. **Use --user flag:**
   ```bash
   pip install --user -r requirements.txt
   ```

---

## Application Launch Problems

### Problem: Application window doesn't open

**Symptoms:**
- Double-clicking `Run BuildSmartOS.bat` does nothing
- Command prompt flashes and closes

**Solutions:**

1. **Check for error messages:**
   - Open Command Prompt manually
   - Navigate to folder:
     ```bash
     cd C:\Users\ASUS\Desktop\Business\BuildSmartOS
     ```
   - Run:
     ```bash
     python main.py
     ```
   - Read error messages

2. **Verify Python installation:**
   ```bash
   python --version
   # Should show 3.8 or higher
   ```

3. **Check database existence:**
   - Look for `buildsmart_hardware.db` in folder
   - If missing, run:
     ```bash
     python database_setup.py
     ```

### Problem: "ImportError: No module named customtkinter"

**Symptoms:**
- Error message about missing customtkinter
- Application won't start

**Solution:**

```bash
pip install customtkinter
```

If still fails:
```bash
pip install --upgrade customtkinter
```

### Problem: Application starts but window is blank/white

**Symptoms:**
- Window opens but no content
- White screen or grey screen

**Solutions:**

1. **Update customtkinter:**
   ```bash
   pip install --upgrade customtkinter
   ```

2. **Check Python version:**
   - Ensure Python 3.8+
   - CustomTkinter requires newer Python

3. **Try different appearance mode:**
   - Edit `main.py`
   - Change line:
     ```python
     ctk.set_appearance_mode("Light")  # Instead of "Dark"
     ```

### Problem: "Database is locked" error

**Symptoms:**
- Error message: "database is locked"
- Application freezes on startup

**Solutions:**

1. **Close all instances:**
   - Press `Ctrl + Shift + Esc` (Task Manager)
   - Find all "python.exe" processes
   - End them
   - Restart application

2. **Check for orphaned lock:**
   - Look for `buildsmart_hardware.db-journal` file
   - Delete it if exists
   - Restart application

3. **Restore from backup:**
   ```bash
   # Backup current (possibly corrupt) database
   copy buildsmart_hardware.db buildsmart_hardware.db.corrupt
   
   # Restore from backup
   copy backups\latest_backup.db buildsmart_hardware.db
   ```

---

## Database Issues

### Problem: Database file missing after application use

**Symptoms:**
- Database was working before
- Now `buildsmart_hardware.db` is missing

**Solutions:**

1. **Check backups folder:**
   - Open `backups/` directory
   - Find most recent backup
   - Copy to main folder:
     ```bash
     copy backups\backup_YYYYMMDD_HHMMSS.db buildsmart_hardware.db
     ```

2. **Recreate database:**
   ```bash
   python database_setup.py
   ```
   - **Warning:** This creates empty database, all data lost if no backup

### Problem: "Could not open database file" error

**Symptoms:**
- Error accessing database
- Permissions error

**Solutions:**

1. **Check file permissions:**
   - Right-click `buildsmart_hardware.db`
   - Properties → Security
   - Ensure your user has Full Control

2. **Run as Administrator:**
   - Right-click `Run BuildSmartOS.bat`
   - "Run as Administrator"

3. **Move to different location:**
   - Copy entire BuildSmartOS folder to `C:\BuildSmartOS`
   - Try running from there

### Problem: Database corruption - "database disk image is malformed"

**Symptoms:**
- Error message about malformed database
- Application crashes when accessing data

**Solutions:**

1. **Try database recovery:**
   ```bash
   sqlite3 buildsmart_hardware.db ".recover" > recovered.sql
   sqlite3 buildsmart_new.db < recovered.sql
   ```

2. **Validate database:**
   ```bash
   python database_validator.py
   ```
   - Follow repair instructions

3. **Restore from backup:**
   - Use most recent backup from `backups/` folder

### Problem: Missing products/customers/transactions after update

**Symptoms:**
- Data was present before
- Now missing after application restart

**Solutions:**

1. **Check database integrity:**
   ```bash
   python database_validator.py
   ```

2. **Verify correct database file:**
   - Ensure only one `buildsmart_hardware.db`
   - Check no duplicate databases in different folders

3. **Restore from backup:**
   - Check `backups/` for recent backup
   - Compare file sizes (larger = more data)

---

## Feature-Specific Issues

### Problem: WhatsApp not sending invoices

**Symptoms:**
- Checkbox checked but no WhatsApp opens
- WhatsApp opens but message not sent

**Solutions:**

1. **Ensure WhatsApp Web logged in:**
   - Open browser
   - Go to web.whatsapp.com
   - Scan QR code with phone
   - Keep browser window open

2. **Check phone number format:**
   - Should be: 0771234567 (Sri Lanka)
   - No spaces or dashes
   - Include country code if international

3. **Verify pywhatkit installed:**
   ```bash
   pip install pywhatkit
   ```

4. **Allow time for WhatsApp to open:**
   - Wait 10-15 seconds after checkout
   - Don't close browser window

**Alternative:**
- Manually send invoice PDF from `bills/` folder

### Problem: PDF invoices not generating

**Symptoms:**
- Checkout completes but no PDF file
- `bills/` folder empty

**Solutions:**

1. **Verify reportlab installed:**
   ```bash
   pip install reportlab
   ```

2. **Check folder permissions:**
   - Ensure `bills/` folder exists
   - Create if missing:
     ```bash
     mkdir bills
     ```

3. **Run as Administrator:**
   - May need elevated permissions to create files

4. **Check disk space:**
   - Ensure sufficient free space (at least 100MB)

### Problem: Analytics dashboard not working

**Symptoms:**
- Button clicks but nothing happens
- Error about matplotlib

**Solutions:**

1. **Install analytics packages:**
   ```bash
   pip install matplotlib pandas numpy
   ```

2. **Check for data:**
   - Analytics requires transactions
   - Generate test data:
     ```bash
     python generate_test_data.py
     ```

3. **Update matplotlib:**
   ```bash
   pip install --upgrade matplotlib
   ```

### Problem: Barcode scanner not working

**Symptoms:**
- Camera doesn't open
- Error about opencv

**Solutions:**

1. **Install barcode packages:**
   ```bash
   pip install opencv-python pyzbar
   ```

2. **Check camera permissions:**
   - Windows Settings → Privacy → Camera
   - Allow desktop apps to access camera

3. **Test camera:**
   - Open Camera app to verify camera works
   - Close Camera app before using barcode scanner

4. **Update drivers:**
   - Update webcam drivers in Device Manager

### Problem: Voice commands not responding

**Symptoms:**
- Microphone button does nothing
- No speech recognition

**Solutions:**

1. **Install voice packages:**
   ```bash
   pip install SpeechRecognition pyttsx3
   ```

2. **Check microphone:**
   - Windows Settings → Privacy → Microphone
   - Allow desktop apps to access microphone

3. **Test microphone:**
   - Use Windows Voice Recorder
   - Verify microphone works

4. **Internet connection:**
   - Voice recognition requires internet
   - Check connection

### Problem: Multi-language not switching

**Symptoms:**
- Language dropdown exists but doesn't change UI
- UI stays in English

**Solutions:**

1. **Check translation files:**
   - Verify `translations/` folder exists
   - Files: english.json, sinhala.json, tamil.json

2. **Verify language_manager:**
   ```bash
   python -c "from language_manager import translate; print(translate('test'))"
   ```

3. **Restart application:**
   - Language changes may require restart

---

## Performance Problems

### Problem: Application is very slow

**Symptoms:**
- Buttons take seconds to respond
- Scrolling is laggy
- UI freezes

**Solutions:**

1. **Reduce product count:**
   - Archive old products
   - Keep < 5,000 active products

2. **Close other programs:**
   - Free up RAM
   - Close browser, other apps

3. **Clean transaction history:**
   - Archive transactions older than 2 years
   - Keep database lean

4. **Check CPU usage:**
   - Task Manager → Performance
   - If high, identify culprit program

5. **Upgrade hardware:**
   - Minimum: 4GB RAM, i3 processor
   - Recommended: 8GB RAM, i5 processor

### Problem: Database queries taking long time

**Symptoms:**
- Search takes 10+ seconds
- Reports take minutes to generate

**Solutions:**

1. **Run database optimizer:**
   ```bash
   sqlite3 buildsmart_hardware.db "VACUUM;"
   ```

2. **Check indexes:**
   ```bash
   python database_validator.py
   ```
   - Should show 16+ indexes

3. **Reduce transaction count:**
   - Archive old transactions
   - Keep recent data only

### Problem: High memory usage

**Symptoms:**
- Task Manager shows BuildSmartOS using lots of RAM
- Computer slows down

**Solutions:**

1. **Close extra windows:**
   - Only keep main window open
   - Close Product Manager when not using

2. **Restart application daily:**
   - Close and reopen to free memory

3. **Upgrade RAM:**
   - 8GB recommended for large databases

---

## Integration Issues

### Problem: Cloud backup not working

**Symptoms:**
- Backup to Google Drive fails
- Authentication errors

**Solutions:**

1. **Check API credentials:**
   - Verify `config.json` has correct API key
   - Regenerate if expired

2. **Internet connection:**
   - Ensure stable internet
   - Check firewall settings

3. **Manual backup:**
   - Copy `buildsmart_hardware.db` to Google Drive manually
   - Use `backups/` folder

### Problem: QR code generation fails

**Symptoms:**
- QR codes don't appear
- Error about qrcode module

**Solution:**

```bash
pip install qrcode[pil]
```

---

## Common Error Messages

### "AttributeError: 'NoneType' object has no attribute"

**Cause:** Trying to access database before connection established

**Solution:**
- Restart application
- Ensure database exists
- Run `python database_setup.py`

### "sqlite3.OperationalError: no such table"

**Cause:** Database missing tables

**Solution:**
```bash
python database_setup.py
```

### "ValueError: invalid literal for int() with base 10"

**Cause:** Invalid data entry (text in number field)

**Solution:**
- Enter only numbers in price/stock fields
- Use decimal point for prices (e.g., 150.50)

### "KeyError: 'business'"

**Cause:** `config.json` missing or corrupt

**Solution:**

Create `config.json` with:
```json
{
  "business": {
    "name": "Your Store",
    "address": "Your Address",
    "phone": "077-1234567"
  },
  "settings": {
    "default_language": "english",
    "theme": "dark"
  }
}
```

### "UnicodeDecodeError"

**Cause:** Character encoding issue (usually Sinhala/Tamil text)

**Solution:**
- Save files with UTF-8 encoding
- Ensure language files are UTF-8

---

## Getting Additional Help

### Diagnostic Information to Collect

When reporting issues, provide:

1. **System Information:**
   ```bash
   python --version
   pip list
   ```

2. **Error Message:**
   - Full error text
   - Screenshot if possible

3. **Steps to Reproduce:**
   - What you clicked
   - What you entered
   - What happened

4. **Environment:**
   - Windows version
   - Python version
   - BuildSmartOS version

### Useful Commands

**Check Python version:**
```bash
python --version
```

**List installed packages:**
```bash
pip list
```

**Database health check:**
```bash
python database_validator.py
```

**Generate test data:**
```bash
python generate_test_data.py
```

**Backup database:**
```bash
python database_setup.py
```

---

## Emergency Recovery

### If All Else Fails

1. **Backup current state:**
   ```bash
   xcopy /E /I BuildSmartOS BuildSmartOS_backup
   ```

2. **Fresh installation:**
   - Download fresh BuildSmartOS
   - Install dependencies
   - Copy `buildsmart_hardware.db` from backup

3. **Contact support:**
   - Email: info@buildsmart.lk
   - Include diagnostic information
   - Attach error screenshots

---

**BuildSmartOS Troubleshooting Guide v1.0**  
*Last Updated: December 15, 2025*  
*Problem Resolution Guide*
