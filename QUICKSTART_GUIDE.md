# BuildSmartOS Quick Start Guide

**Get up and running in 5 minutes!**

---

## 🚀 Installation (2 minutes)

### Step 1: Install Dependencies

Open Command Prompt in the BuildSmartOS folder:

```bash
pip install customtkinter reportlab matplotlib pandas numpy qrcode
```

### Step 2: Create Database

```bash
python database_setup.py
```

✅ Done! Database created with sample products.

---

## 💻 Launch Application

**Option 1:** Double-click `Run BuildSmartOS.bat`

**Option 2:** Command line:
```bash
python main.py
```

---

## 📦 Make Your First Sale (1 minute)

### Quick Steps:

1. **Find Product** → Type in search box or scroll
2. **Add to Cart** → Click **+** button
3. **Checkout** → Click **CHECKOUT** button
4. **Done!** → PDF invoice saved in `bills/` folder

### With Customer:
1. Click **Add Customer** button
2. Enter phone: `0771234567`
3. Proceed with sale
4. ✅ Loyalty points added automatically

---

## 🎯 Essential Features

### Product Management

📦 **Click "Products" button** → Add/Edit/Delete products

```
Add Product:
- Name: Portland Cement 50kg
- Category: Cement
- Price: 1250.00
- Unit: bag
- Stock: 100
→ Click Save
```

### View Reports

📄 **Click "Reports" button** → Select report type → Generate

**Popular Reports:**
- Daily Sales Report
- Low Stock Report
- Top Products Report

### Analytics Dashboard

📊 **Click "Analytics" button** → View:
- Today's sales
- Monthly revenue
- Top products
- Sales trends

---

## 🔧 Configuration

Edit `config.json`:

```json
{
  "business": {
    "name": "Your Store Name",
    "address": "123 Main St, Colombo",
    "phone": "077-1234567"
  }
}
```

---

## 📱 Quick Features

| Feature | How to Use |
|---------|------------|
| **Search** | Type product name in search box |
| **Language** | Dropdown menu: English / සිංහල / தமிழ் |
| **WhatsApp** | Check box before checkout |
| **Daily Report** | Reports → Daily Sales → Generate |
| **Add Stock** | Products → Edit → Update stock |

---

## 🔑 Shortcuts & Tips

### Fastest Sale Process:
```
Search → + → Add Customer → Checkout
```
⏱️ **Under 30 seconds!**

### Daily Routine:
1. Morning: Check low stock alert
2. During day: Process sales
3. Evening: Generate daily report

### Best Practices:
- ✅ Always add customer phone for loyalty
- ✅ Check low stock daily
- ✅ Backup database weekly
- ✅ Update stock when receiving deliveries

---

## 📊 Understanding the Interface

```
┌─────────────────────────────────────────────┐
│ Products │ Customers │ Reports │ Analytics  │ ← Top Bar
├──────────────────────┬──────────────────────┤
│ Product List         │ Shopping Cart        │
│ [Search Box]         │ Item 1    LKR 500    │
│                      │ Item 2    LKR 1200   │
│ Category: Cement     │ ──────────────────   │
│ Portland Cement      │ Total:    LKR 1700   │
│ LKR 1250/bag [+]     │                      │
│                      │ [ ] Send WhatsApp    │
│ Category: Paint      │ [Add Customer]       │
│ Red Paint 1L         │ [ CHECKOUT ]         │
│ LKR 450/liter [+]    │                      │
└──────────────────────┴──────────────────────┘
```

---

## ❓ Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Window doesn't open | Run: `python main.py` to see errors |
| No products showing | Run: `python database_setup.py` |
| Can't checkout | Make sure cart has items |
| PDF not generating | Check `bills/` folder exists |
| WhatsApp not working | Login to web.whatsapp.com |

**More help:** See `TROUBLESHOOTING.md`

---

## 📚 Learn More

- **Full Manual:** `USER_MANUAL.md` - Complete feature guide
- **For Developers:** `DEVELOPER_GUIDE.md` - Code documentation
- **Fix Problems:** `TROUBLESHOOTING.md` - Common issues

---

## 🎉 You're Ready!

BuildSmartOS is now set up and ready to use.

**Test the system:**
1. ✅ Add a product
2. ✅ Make a test sale  
3. ✅ Generate a report  
4. ✅ View analytics

**Next Steps:**
- Add your real products
- Configure business info in `config.json`
- Set reorder levels for stock alerts
- Start making sales!

---

**Need Help?**  
📧 info@buildsmart.lk  
📱 077-1234567

---

*BuildSmartOS - Smart POS for Sri Lankan Hardware Stores*  
*Version 1.0 | Last Updated: December 15, 2025*
