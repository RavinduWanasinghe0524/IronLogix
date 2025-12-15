# 🏪 BuildSmartOS - Sri Lanka's First Smart Hardware POS System

![Production Ready](https://img.shields.io/badge/Status-Production%20Ready-brightgreen) ![Tests Passing](https://img.shields.io/badge/Tests-27%2F27%20Passing-success) ![Python](https://img.shields.io/badge/Python-3.8%2B-blue)

**🎉 Phase 2 Complete!** All automated tests passed (100% success rate). System is production-ready.

## Overview

BuildSmartOS is a revolutionary point-of-sale system designed specifically for Sri Lankan hardware stores. It combines traditional POS functionality with cutting-edge AI, multi-language support, and business intelligence features.

## 🌟 Key Features

### Multi-Language Support
- **Sinhala, Tamil, and English** interface
- Real-time language switching
- Unicode support for native scripts

### WhatsApp Integration 📱
- Send invoices directly to customers via WhatsApp
- Automated low-stock alerts
- Professional message formatting

### AI-Powered Analytics 🤖
- Sales predictions using machine learning
- Automated reorder recommendations
- Trend analysis and forecasting

### Voice Control 🎤
- Hands-free operation
- Commands in Sinhala, Tamil, and English
- Text-to-speech feedback

### Barcode/QR Scanning
- Instant product lookup
- Camera-based scanning
- QR code generation for products

### Customer Loyalty Program 🎁
- Automatic points tracking
- Rewards system
- Customer purchase history

### Construction Estimator 🏗️
- Project cost calculator
- Sri Lankan market-specific templates
- Material quantity estimation

### Business Intelligence 📊
- Real-time sales dashboard
- Profit margin analysis
- Top-selling products reports
- Sales trend charts

### Additional Features
- Credit customer management
- Supplier database
- Expense tracking
- Cloud backup support
- Professional PDF invoices
- Touch-optimized interface

## 📋 Requirements

### System Requirements
- Windows 10 or later
- Python 3.8+
- Webcam (for barcode scanning)
- Microphone (for voice commands)
- Internet connection (for WhatsApp, cloud backup)

### Python Dependencies
```bash
pip install -r requirements.txt
```

## 📚 Documentation

**Quick Start:**
- 📖 [Quick Start Guide](QUICKSTART_GUIDE.md) - Get running in 5 minutes
- 📘 [User Manual](USER_MANUAL.md) - Complete feature guide
- 🔧 [Troubleshooting Guide](TROUBLESHOOTING.md) - Fix common issues

**For Developers:**
- 💻 [Developer Guide](DEVELOPER_GUIDE.md) - Architecture & API docs
- ✅ [Phase 1 Report](PHASE1_COMPLETE.md) - Setup completion
- 📊 [Phase 2 Test Report](PHASE2_TEST_REPORT.md) - Testing results (100% pass)

## 🚀 Quick Start

### 1. Database Setup
```bash
python database_setup.py
```

### 2. Configuration
Edit `config.json` to customize:
- Business information
- Default language
- Feature toggles
- API keys

### 3. Run Application
```bash
python main.py
```

## 📱 WhatsApp Setup

1. **Method 1: Using pywhatkit (Free)**
   - No API key required
   - Uses WhatsApp Web
   - Manual QR code scan on first use

2. **Method 2: WhatsApp Business API (Paid)**
   - Add API key to `config.json`
   - Fully automated sending

## 🎨 Usage Guide

### Basic Sale
1. Browse products or use search
2. Click "+" to add items to cart
3. Click "CHECKOUT" to complete sale
4. Optionally send invoice via WhatsApp

### Voice Commands
- "Add cement to cart"
- "Search for paint"
- "What's the total?"
- "Checkout"

### Barcode Scanning
- Click barcode icon
- Point camera at barcode/QR code
- Product automatically added

### Construction Estimates
1. Open estimator tool
2. Select project type
3. Enter area
4. Get instant material list and costs

### Analytics
- View sales dashboard
- Generate reports
- Analyze trends
- Check profit margins

## 🔧 Configuration

### config.json Structure
```json
{
  "business": {
    "name": "Your Store Name",
    "address": "Store Address",
    "phone": "077-1234567"
  },
  "settings": {
    "default_language": "english",
    "theme": "dark"
  },
  "features": {
    "whatsapp_enabled": true,
    "voice_enabled": true,
    "barcode_enabled": true
  }
}
```

## 📊 Database Schema

- **products**: Product inventory
- **customers**: Customer database with loyalty points
- **transactions**: Sales records
- **sales_items**: Transaction line items
- **suppliers**: Supplier information
- **loyalty_transactions**: Points history
- **credit_sales**: Credit tracking
- **expenses**: Business expenses

## 🛠️ Development

### Project Structure
```
BuildSmartOS/
├── main.py                      # Main application
├── database_setup.py            # Database initialization
├── pdf_generator.py             # Invoice generation
├── language_manager.py          # Multi-language support
├── whatsapp_service.py          # WhatsApp integration
├── barcode_scanner.py           # Barcode/QR scanning
├── voice_assistant.py           # Voice commands
├── loyalty_manager.py           # Loyalty program
├── ai_predictor.py              # AI predictions
├── analytics_dashboard.py       # Analytics
├── construction_estimator.py    # Cost estimator
├── themes.py                    # UI themes
├── config.json                  # Configuration
├── requirements.txt             # Dependencies
├── translations/                # Language files
│   ├── english.json
│   ├── sinhala.json
│   └── tamil.json
├── bills/                       # Generated invoices
├── reports/                     # Analytics reports
└── models/                      # AI models

```

## 🌐 Localization

Add new languages by:
1. Create `translations/language_name.json`
2. Copy structure from `english.json`
3. Translate all values
4. Update `language_manager.py`

## 🔐 Security

- Local SQLite database
- Optional cloud backup encryption
- Customer data privacy
- Secure API key storage

## ✅ Testing & Quality Assurance

**Phase 2 Testing Complete: 100% Success Rate**

- **Total Tests:** 27 automated tests
- **Pass Rate:** 27/27 (100%)
- **Test Coverage:**
  - ✅ Core functionality (10/10)
  - ✅ Product management (5/5)
  - ✅ Customer management (5/5)
  - ✅ Analytics dashboard (7/7)

**Database Health:**
- 8 tables fully operational
- 16 performance indexes active
- 2 data integrity triggers working
- No data corruption detected

**Test Reports:**
- [Phase 2 Test Report](PHASE2_TEST_REPORT.md) - Detailed results
- [Manual Testing Guide](MANUAL_TESTING_GUIDE.md) - UI testing procedures

## 📈 Roadmap

- [ ] Mobile app (Android/iOS)
- [ ] Web dashboard
- [ ] Multi-store support
- [ ] Advanced reporting
- [ ] Integration with accounting software
- [ ] Email invoicing
- [ ] SMS notifications

## 💡 Tips

1. **First Launch**: Complete database setup
2. **Regular Backups**: Enable cloud backup
3. **Train AI**: Import historical sales for better predictions
4. **Update Stock**: Regular inventory counts
5. **Customer Loyalty**: Encourage phone number collection

## 🐛 Troubleshooting

### Voice Commands Not Working
- Check microphone permissions
- Verify internet connection (uses Google Speech API)
- Test with English first

### WhatsApp Not Sending
- Ensure WhatsApp Web is logged in
- Check internet connection
- Verify phone number format

### Barcode Scanner Issues
- Allow camera permissions
- Ensure good lighting
- Hold barcode steady

## 📞 Support

- Email: info@buildsmart.lk
- Website: buildsmart.lk
- Phone: 077-1234567

## 📄 License

Proprietary - BuildSmart OS
© 2024 BuildSmart Technologies

## 🙏 Acknowledgments

Built with:
- CustomTkinter for modern UI
- ReportLab for PDF generation
- scikit-learn for AI predictions
- OpenCV for barcode scanning
- pywhatkit for WhatsApp integration

---

**Made with ❤️ in Sri Lanka**
