# 📦 Installation Guide - BuildSmartOS

## Quick Installation

### Method 1: Automatic (Recommended)

**Double-click:** `INSTALL.bat`

That's it! The installer will:
- ✅ Check Python installation
- ✅ Install all required packages
- ✅ Setup database
- ✅ Initialize license (30-day trial)
- ✅ Create necessary folders

**Time:** 2-5 minutes

---

### Method 2: Manual Installation

If automatic installation fails:

**Step 1: Check Python**
```bash
python --version
```
Must show Python 3.8 or higher.

**Step 2: Install Packages**
```bash
pip install -r requirements.txt
```

**Step 3: Setup Database**
```bash
python database_setup.py
```

**Step 4: Create Folders**
```bash
mkdir backups bills reports logs
```

**Step 5: Run Application**
```bash
python main.py
```

---

## System Requirements

### Minimum:
- **OS:** Windows 7 or higher
- **RAM:** 2GB
- **Storage:** 500MB free space
- **Python:** 3.8 or higher
- **Internet:** For installation and WhatsApp

### Recommended:
- **OS:** Windows 10/11
- **RAM:** 4GB
- **Storage:** 1GB free space
- **Python:** 3.10 or higher
- **Internet:** Broadband connection

---

## Installation Steps (Detailed)

### 1. Python Installation

**If Python is not installed:**

1. Download from: https://www.python.org/downloads/
2. Run installer
3. **IMPORTANT:** Check "Add Python to PATH"
4. Click "Install Now"
5. Wait for completion
6. Restart command prompt

**Verify:**
```bash
python --version
pip --version
```

### 2. BuildSmartOS Installation

1. Extract BuildSmartOS folder
2. Open folder
3. Double-click `INSTALL.bat`
4. Wait for installation (2-5 minutes)
5. Installation complete!

---

## What Gets Installed

### Python Packages:
```
✓ customtkinter    - Modern UI
✓ reportlab        - PDF generation
✓ pywhatkit        - WhatsApp integration
✓ deep-translator  - Multi-language
✓ matplotlib       - Charts & graphs
✓ pandas           - Data analysis
✓ scikit-learn     - AI predictions
```

### Files Created:
```
✓ buildsmart_hardware.db  - Database
✓ license.json            - License data
✓ backups/                - Backup folder
✓ bills/                  - PDF bills
✓ reports/                - Reports
✓ logs/                   - System logs
```

---

## Troubleshooting Installation

### Error: "Python is not installed"
**Solution:**
1. Install Python from python.org
2. Make sure "Add to PATH" is checked
3. Restart computer
4. Try again

### Error: "pip install failed"
**Solution:**
```bash
# Try upgrading pip
python -m pip install --upgrade pip

# Install packages one by one
pip install customtkinter
pip install reportlab
pip install pywhatkit
```

### Error: "Database setup failed"
**Solution:**
```bash
# Delete old database if exists
del buildsmart_hardware.db

# Run setup again
python database_setup.py
```

### Error: "Permission denied"
**Solution:**
1. Right-click `INSTALL.bat`
2. Choose "Run as Administrator"
3. Try again

### Error: "Internet connection required"
**Solution:**
- Check internet connection
- Try again with good connection
- Or download packages offline

---

## First Run

After installation:

**1. Start Application:**
```bash
# Double-click:
Run BuildSmartOS.bat

# Or command:
python main.py
```

**2. First Launch:**
- Application opens
- 30-day trial starts automatically
- Machine ID generated
- License dialog may appear

**3. Initial Setup:**
- Choose language (English/Sinhala/Tamil)
- Configure business details in settings
- Add your first products
- Ready to use!

---

## Verification

**Check if everything works:**

1. **Application Starts:**
   - Run BuildSmartOS.bat
   - Main window appears
   - No errors shown

2. **Database Works:**
   - Can add products
   - Can view inventory
   - Data saves correctly

3. **License Active:**
   - Top bar shows "Trial: X days remaining"
   - All features accessible

4. **PDF Generation:**
   - Process a test transaction
   - PDF bill generates in bills/ folder

5. **WhatsApp (Optional):**
   - Login to WhatsApp Web
   - Test invoice sending
   - Message delivers

---

## Clean Installation

**If you need to start fresh:**

```bash
# 1. Backup your data
python -m shutil copy buildsmart_hardware.db backup.db

# 2. Delete files
del license.json
del buildsmart_hardware.db

# 3. Reinstall
INSTALL.bat
```

---

## Installation for Multiple Computers

**To install on another computer:**

1. Copy entire BuildSmartOS folder
2. Transfer to new computer (USB/Network)
3. Run `INSTALL.bat`
4. New 30-day trial starts
5. Different Machine ID generated
6. Need separate activation code

---

## Offline Installation

**If target computer has no internet:**

1. **On Internet-Connected Computer:**
   ```bash
   # Download packages
   pip download -r requirements.txt -d packages/
   ```

2. **Copy to Target Computer:**
   - Copy packages/ folder
   - Copy BuildSmartOS folder

3. **Install Offline:**
   ```bash
   # Install from local packages
   pip install --no-index --find-links=packages/ -r requirements.txt
   ```

---

## Post-Installation

### Recommended Steps:

1. **Configure Business Details:**
   - Open config.json
   - Update business name, address, phone
   - Save changes

2. **Test Core Features:**
   - Add sample products
   - Process test transaction
   - Generate PDF bill
   - Verify everything works

3. **Setup WhatsApp:**
   - Open browser
   - Go to web.whatsapp.com
   - Scan QR code
   - Keep logged in

4. **Create Backup:**
   - Double-click `Backup Database.bat`
   - Verify backup created
   - Test restoration

5. **Read Documentation:**
   - USER_MANUAL.md - Full guide
   - TROUBLESHOOTING.md - Common issues
   - LICENSE_SYSTEM_GUIDE.md - Trial & activation

---

## Quick Start After Installation

```bash
# 1. Start application
Run BuildSmartOS.bat

# 2. Add products (📦 Products button)
# 3. Add customer (👥 Add Customer)
# 4. Process sale (Add to cart, Checkout)
# 5. Generate PDF and WhatsApp invoice

# That's it! You're ready to go!
```

---

## Need Help?

**During Installation:**
- Read error messages carefully
- Check Python version: `python --version`
- Check pip works: `pip --version`
- Run as Administrator if needed

**After Installation:**
- Read: USER_MANUAL.md
- Read: TROUBLESHOOTING.md
- Contact: 077-XXXXXXX
- Email: support@buildsmart.lk

---

## Updates

**To update BuildSmartOS:**

1. Backup your data first!
2. Download new version
3. Replace all files EXCEPT:
   - buildsmart_hardware.db
   - license.json
   - config.json
4. Run application

---

**Installation should take 2-5 minutes. Enjoy BuildSmartOS!** 🚀
