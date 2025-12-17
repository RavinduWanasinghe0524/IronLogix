# 📦 BuildSmartOS - Installation Guide

## Quick Install (Windows)

### Method 1: Download Installer (Recommended)
1. **Download** `BuildSmartOS-Setup.exe` from [GitHub Releases]
2. **Run** the installer
3. **Follow** the setup wizard
4. **Done!** Launch from desktop shortcut

### Method 2: Build from Source

#### Prerequisites
- Windows 10 or later
- Python 3.8+ installed
- Internet connection

#### Steps
```bash
# 1. Clone or download the repository
git clone https://github.com/RavinduWanasinghe0524/IronLogix.git
cd BuildSmartOS

# 2. Run automated installer
python setup_installer.py

# 3. Launch application
python main.py
```

---

## First-Time Setup Wizard

After installation, the **Setup Wizard** will guide you through:

### Step 1: Welcome
Quick overview of BuildSmartOS features

### Step 2: Business Information
- Business name
- Address
- Phone number
- Email

### Step 3: Preferences
- Default language (English/Sinhala/Tamil)
- Theme (Dark/Light)
- Sample data option

### Step 4: **Initial Inventory** ⭐ NEW!
Add your starter products during install:
- Product name
- Price (LKR)
- Stock quantity
- Category

**Example:**
- Cement 50kg - LKR 1850 - Stock: 50 - Category: Cement
- Clay Bricks - LKR 25 - Stock: 500 - Category: Bricks
- Metal Chips - LKR 4500 - Stock: 20 - Category: Aggregates

**Tip:** Skip this step if you prefer to add products later from the Products menu

### Step 5: Optional Features
Enable/disable:
- WhatsApp invoice sending
- Voice commands
- Barcode scanner
- Cloud backup

### Step 6: Summary
Review your configuration and finish!

---

## System Requirements

**Minimum:**
- Windows 10 (64-bit)
- 4 GB RAM
- 500 MB disk space
- 1280x720 display

**Recommended:**
- Windows 11
- 8 GB RAM
- 1 GB disk space (for data)
- 1920x1080 display
- Webcam (for barcode scanning)
- Microphone (for voice commands)

---

## Post-Installation

### 1. Test the Application
- Add a few test products
- Create a test sale
- Generate a PDF invoice
- Try the refund manager

### 2. Configure WhatsApp (Optional)
- Enable WhatsApp in settings
- Log into WhatsApp Web on your default browser
- Test invoice sending

### 3. Backup Your Data
- Use "Backup Database.bat" regularly
- Enable cloud backup in config.json
- Keep backups in multiple locations

### 4. Customize
- Edit `config.json` for advanced settings
- Add your business logo
- Adjust loyalty program parameters

---

## Troubleshooting

### Application won't start
- Ensure Python 3.8+ is installed
- Run: `python verify_dependencies.py`
- Check `logs/` folder for errors

### Database error
- Run: `python database_setup.py`
- Check file permissions
- Ensure disk space available

### WhatsApp not sending
- Log into WhatsApp Web
- Check internet connection
- Verify phone number format (+94...)

### PDF generation fails
- Install: `pip install reportlab`
- Check write permissions to `bills/` folder

---

## Uninstallation

**Installed Version:**
- Control Panel → Programs → Uninstall BuildSmartOS

**Source Version:**
- Simply delete the BuildSmartOS folder
- Backup `buildsmart_hardware.db` first!

---

## Getting Help

📚 **Documentation:** See USER_MANUAL.md
🐛 **Issues:** GitHub Issues
💬 **Community:** [Discord/Telegram]
📧 **Email:** info@buildsmart.lk

---

## Next Steps

1. ✅ Complete setup wizard
2. ✅ Add your products
3. ✅ Create test transactions
4. ✅ Explore analytics dashboard
5. ✅ Set up WhatsApp integration
6. ✅ Train your staff
7. ✅ Go live!

**Welcome to BuildSmartOS! 🚀**
