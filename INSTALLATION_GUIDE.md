# BuildSmartOS Installation Guide

**Complete step-by-step installation instructions**

---

## System Requirements

### Minimum Requirements
- **Operating System:** Windows 10 or later (64-bit)
- **Python:** Version 3.8 or higher
- **RAM:** 4GB minimum (8GB recommended)
- **Storage:** 500MB free space
- **Display:** 1280x720 minimum resolution

### Optional Hardware
- **Webcam:** For barcode scanning feature
- **Microphone:** For voice commands feature
- **Internet Connection:** For WhatsApp integration and cloud backup

---

## Installation Methods

### Method 1: Automated Installation (Recommended)

**For Users Without Python Installed:**

1. **Download and Install Python:**
   - Visit: https://www.python.org/downloads/
   - Download Python 3.11 or later
   - ✅ **IMPORTANT:** Check "Add Python to PATH" during installation
   - Complete installation

2. **Extract BuildSmartOS:**
   - Extract the BuildSmartOS ZIP file to desired location
   - Example: `C:\BuildSmartOS`

3. **Run Installer:**
   - Double-click `Install BuildSmartOS.bat`
   - Wait for automatic installation (5-10 minutes)
   - Follow on-screen prompts

4. **Complete Setup:**
   - Configuration wizard will launch automatically
   - Enter your business information
   - Choose preferences
   - Click "Finish"

5. **Launch Application:**
   - Double-click `Run BuildSmartOS.bat`
   - Or use desktop shortcut "BuildSmartOS"

---

### Method 2: Manual Installation

**For Advanced Users:**

1. **Open Command Prompt:**
   ```batch
   cd C:\Path\To\BuildSmartOS
   ```

2. **Install Dependencies:**
   ```bash
   pip install customtkinter reportlab matplotlib pandas numpy qrcode[pil]
   ```

3. **Setup Database:**
   ```bash
   python database_setup.py
   ```

4. **Generate Sample Data (Optional):**
   ```bash
   python generate_test_data.py
   ```

5. **Create Configuration:**
   ```bash
   python first_run_wizard.py
   ```

6. **Create Shortcuts (Optional):**
   ```bash
   python create_shortcuts.py
   ```

7. **Launch Application:**
   ```bash
   python main.py
   ```

---

## First-Run Configuration Wizard

The wizard will guide you through 5 steps:

### Step 1: Welcome
- Introduction to BuildSmartOS
- Overview of setup process

### Step 2: Business Information
Enter your business details:
- **Business Name:** (appears on invoices)
- **Address:** Full business address
- **Phone Number:** Format: 077-1234567
- **Email:** Contact email

### Step 3: Application Preferences
- **Language:** English / සිංහල / தமிழ்
- **Theme:** Dark / Light
- **Sample Data:** Check to generate demo data

### Step 4: Optional Features
Enable or disable:
- ✅ WhatsApp Invoice Sending
- ❌ Voice Commands (requires microphone)
- ❌ Barcode Scanner (requires webcam)
- ❌ Cloud Backup (requires Google Drive)

### Step 5: Summary
- Review your settings
- Click "Finish" to complete setup

---

## Verification Steps

After installation, verify everything works:

### 1. Check Files
Ensure these files exist:
- `buildsmart_hardware.db` - Database file
- `config.json` - Configuration file
- `bills/` - Invoice folder
- `reports/` - Reports folder
- `backups/` - Backup folder

### 2. Test Application
1. Launch BuildSmartOS
2. Check products are loaded (if sample data enabled)
3. Try adding a product to cart
4. Test search functionality

### 3. Check Features
- **Products:** Click "📦 Products" button
- **Customers:** Click "👥 Customers" button
- **Reports:** Click "📄 Reports" button
- **Analytics:** Click "📊 Analytics" button

---

## Troubleshooting Installation

### Problem: "Python is not recognized"

**Solution:**
1. Reinstall Python
2. ✅ Check "Add Python to PATH"
3. Restart computer
4. Try installation again

### Problem: "pip install fails"

**Solution:**
```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Problem: "Database not created"

**Solution:**
```bash
python database_setup.py
```
Check for error messages

### Problem: "Module not found" errors

**Solution:**
```bash
pip install customtkinter reportlab matplotlib pandas numpy qrcode
```

### Problem: Installation very slow

**Solution:**
```bash
pip install --no-cache-dir -r requirements.txt
```

---

## Configuration

### Editing config.json

After installation, you can edit `config.json` to customize:

```json
{
  "business": {
    "name": "Your Store Name",
    "address": "Your Address",
    "phone": "077-1234567",
    "email": "info@yourstore.lk"
  },
  "settings": {
    "default_language": "english",
    "theme": "dark",
    "currency": "LKR"
  },
  "features": {
    "whatsapp_enabled": true,
    "voice_enabled": false,
    "barcode_enabled": false,
    "cloud_backup": false
  }
}
```

**Restart application after editing config.json**

---

## Optional Features Installation

### WhatsApp Integration
1. Already enabled by default
2. Requires WhatsApp Web login
3. Visit web.whatsapp.com and scan QR code

### Voice Commands
```bash
pip install SpeechRecognition pyttsx3
```
Then enable in config.json

### Barcode Scanner
```bash
pip install opencv-python pyzbar
```
Then enable in config.json

### Cloud Backup
```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```
Configure Google Drive API credentials

---

## Uninstallation

### Remove BuildSmartOS

1. **Backup Data:**
   - Copy `buildsmart_hardware.db` to safe location
   - Copy `bills/` and `reports/` folders

2. **Delete Files:**
   - Delete BuildSmartOS folder
   - Remove desktop shortcuts

3. **Uninstall Python (Optional):**
   - Only if not needed for other programs
   - Control Panel → Add/Remove Programs

---

## Upgrading BuildSmartOS

### Upgrade Process

1. **Backup Current Version:**
   ```batch
   Backup Database.bat
   ```

2. **Download New Version:**
   - Extract to temporary folder

3. **Copy Data Files:**
   - Copy `buildsmart_hardware.db` to new version
   - Copy `config.json` to new version
   - Copy `bills/` and `reports/` folders

4. **Test New Version:**
   - Run in new folder
   - Verify data intact

5. **Replace Old Version:**
   - Delete old folder
   - Rename new folder

---

## Network Installation (Multiple Computers)

### Shared Database Setup

1. **Install on Server:**
   - Follow standard installation
   - Share BuildSmartOS folder on network

2. **Client Setup:**
   - Map network drive to shared folder
   - Create shortcut on client desktop
   - Point to network `Run BuildSmartOS.bat`

**Note:** SQLite has limitations for concurrent access. For heavy multi-user environments, consider database upgrade.

---

## Getting Help

### Documentation
- **Quick Start:** QUICKSTART_GUIDE.md
- **User Manual:** USER_MANUAL.md
- **Troubleshooting:** TROUBLESHOOTING.md
- **Developer Guide:** DEVELOPER_GUIDE.md

### Support
- Email: info@buildsmart.lk
- Phone: 077-1234567

---

**Installation Guide v1.0**  
*Last Updated: December 15, 2025*  
*BuildSmartOS - Professional Installation*
