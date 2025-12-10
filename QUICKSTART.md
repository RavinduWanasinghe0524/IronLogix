# 🚀 BuildSmartOS - Quick Start Guide

## Installation & Setup

### Step 1: Install Dependencies
```bash
# Navigate to project directory
cd c:\Users\ASUS\Desktop\Business\BuildSmartOS

# Install all required packages
pip install -r requirements.txt
```

### Step 2: Configure Your Business
Edit `config.json` to add your business details:
```json
{
  "business": {
    "name": "Your Store Name",
    "address": "Your Address",
    "phone": "077-1234567",
    "email": "youremail@example.com"
  }
}
```

### Step 3: Database is Ready!
The database is already set up with:
- ✅ 8 tables created
- ✅ 10 sample products loaded
- ✅ 1 sample supplier
- ✅ 1 sample customer

### Step 4: Run the Application
```bash
python main.py
```

## First Use Tutorial

### Making Your First Sale
1. **Browse Products** - Scroll through the product list
2. **Search** - Use the search box to find items quickly
3. **Add to Cart** - Click the "+" button next to products
4. **Add Customer** (Optional) - Click "Add Customer" to enable WhatsApp & loyalty points
5. **Checkout** - Click the green CHECKOUT button
6. **Invoice** - Automatically saved to `bills/` folder

### Using Multi-Language
- Click the language dropdown in the top bar
- Select: English | Sinhala | Tamil
- Interface updates immediately!

### Viewing Analytics
- Click the "📊 Analytics" button
- See today's sales, monthly totals, top products
- Identify trends and patterns

### Project Estimator
- Click "🏗️ Estimator" button
- Select project type (House, Wall, Roofing)
- Enter area in square feet
- Get instant material list and cost estimate!

## Features Reference

| Feature | How to Use |
|---------|------------|
| **Multi-Language** | Top bar dropdown |
| **Search Products** | Type in search box |
| **WhatsApp Invoice** | Add customer phone, check WhatsApp box |
| **Loyalty Points** | Automatic when customer added |
| **Analytics** | Click Analytics button |
| **Construction Estimator** | Click Estimator button |
| **Voice Commands** | Click 🎤 button (requires mic) |
| **Barcode Scan** | Click 📷 button (requires camera) |

## Sample Products Included

1. Tokyo Super Cement 50kg - LKR 2,300
2. River Sand (Sudda) - LKR 18,000/cube
3. Asbestos Sheet 8ft - LKR 1,200
4. Dulux Brilliant White 4L - LKR 4,500
5. Wiring Cable 1mm - LKR 8,500
6. Steel Bars 12mm - LKR 250/kg
7. Clay Bricks - LKR 25/unit
8. Floor Tiles 2x2 - LKR 150/sqft
9. PVC Pipe 1 inch - LKR 380
10. Electrical Switches - LKR 120

## Adding Your Own Products

Use the database directly or create an admin panel:
```python
# Quick add via database
import sqlite3
conn = sqlite3.connect('buildsmart_hardware.db')
cursor = conn.cursor()
cursor.execute("""
    INSERT INTO products (name, category, price_per_unit, cost_price, stock_quantity, unit_type, barcode)
    VALUES (?, ?, ?, ?, ?, ?, ?)
""", ("Product Name", "Category", 100.00, 80.00, 50, "Unit", "BAR123"))
conn.commit()
conn.close()
```

## Troubleshooting

### Q: Application won't start?
**A:** Make sure you've run `pip install -r requirements.txt`

### Q: No products showing?
**A:** Run `python database_setup.py` to initialize database

### Q: WhatsApp not working?
**A:** On first use, WhatsApp Web will open - scan QR code

### Q: Voice commands not working?
**A:** Check microphone permissions and internet connection

### Q: Want to reset database?
**A:** Delete `buildsmart_hardware.db` and run `python database_setup.py`

## Next Steps

1. **Customize** - Add your own products and suppliers
2. **Train AI** - Import historical sales for better predictions
3. **Configure** - Adjust loyalty points and pricing in config.json
4. **Backup** - Regularly backup `buildsmart_hardware.db`

## Support

For help or questions:
- 📧 Email: info@buildsmart.lk
- 📱 Phone: 077-1234567
- 📖 Read: README.md for detailed documentation

---

**You're all set! 🎉**
Start selling and let BuildSmartOS revolutionize your hardware business!
