# BuildSmartOS User Manual

**Version 1.0 | Production Ready**  
*Sri Lanka's First Smart Hardware POS System*

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Core Features](#core-features)
3. [Advanced Features](#advanced-features)
4. [Daily Operations](#daily-operations)
5. [Reports & Analytics](#reports--analytics)
6. [Tips & Best Practices](#tips--best-practices)

---

## Getting Started

### System Requirements

- **Operating System:** Windows 10 or later
- **Python Version:** 3.8 or higher
- **RAM:** Minimum 4GB (8GB recommended)
- **Storage:** 500MB free space
- **Optional:** Webcam (for barcode scanning), Microphone (for voice commands)

### Installation

#### Step 1: Install Dependencies

Open Command Prompt or PowerShell and navigate to the BuildSmartOS folder:

```bash
cd C:\Users\ASUS\Desktop\Business\BuildSmartOS
```

Install required packages:

```bash
pip install -r requirements.txt
```

**Note:** This will install all essential packages including:
- customtkinter (Modern UI)
- reportlab (PDF generation)
- matplotlib & pandas (Analytics)
- qrcode (QR code generation)

#### Step 2: Initialize Database

Run the database setup script:

```bash
python database_setup.py
```

This will:
- Create `buildsmart_hardware.db` database
- Set up 8 tables with proper indexes and triggers
- Add sample products for testing
- Validate database integrity

#### Step 3: Launch Application

Double-click `Run BuildSmartOS.bat` or run:

```bash
python main.py
```

The application window will open with:
- Product list on the left
- Shopping cart on the right
- Top navigation bar with quick access buttons

### First-Time Setup

#### Configure Business Information

1. Open `config.json` in a text editor
2. Update your business details:

```json
{
  "business": {
    "name": "Your Hardware Store Name",
    "address": "123 Main Street, Colombo",
    "phone": "077-1234567",
    "email": "info@yourstore.lk"
  },
  "settings": {
    "default_language": "english",
    "theme": "dark",
    "currency": "LKR"
  }
}
```

3. Save and restart the application

---

## Core Features

### 1. Making a Sale (Basic Workflow)

#### Step-by-Step Process

**Step 1: Browse Products**
- Products are displayed on the left side, grouped by category
- Each product card shows:
  - Product name
  - Price per unit
  - Available stock
  - Add to cart button (+)

**Step 2: Search for Products**
- Use the search box at the top
- Type product name (e.g., "cement", "paint")
- Products filter in real-time

**Step 3: Add Items to Cart**
- Click the **+** button on any product
- Item appears in the cart panel on the right
- Click **+** multiple times to increase quantity
- Stock levels prevent over-ordering

**Step 4: Add Customer Information (Optional)**
- Click **"Add Customer"** button
- Enter customer phone number (format: 0771234567)
- Customer earns loyalty points automatically
- Button shows customer phone after adding

**Step 5: Review Cart**
- Check items and quantities
- Verify subtotal and total
- Remove items with **✖** button if needed

**Step 6: Checkout**
- Click **"CHECKOUT"** button
- Success message appears with invoice details
- PDF invoice automatically generated in `bills/` folder
- Cart clears automatically
- Stock levels update

**Step 7: Send Invoice (Optional)**
- Check **"Send WhatsApp"** before checkout
- Invoice sent to customer via WhatsApp
- Requires WhatsApp Web to be logged in

### 2. Product Management

Access product management by clicking **"📦 Products"** in the top bar.

#### Adding a New Product

1. Click **"Add Product"** button
2. Fill in the form:
   - **Product Name:** (e.g., "Portland Cement 50kg")
   - **Category:** (e.g., "Cement", "Paint", "Tools")
   - **Price:** Unit price in LKR
   - **Unit:** (e.g., "bag", "kg", "liter", "piece")
   - **Stock:** Available quantity
   - **Reorder Level:** Low stock alert threshold
   - **Supplier:** (Optional)
3. Click **"Save"**

#### Editing a Product

1. Find the product in the list
2. Click **"Edit"** button
3. Update details
4. Click **"Save Changes"**

#### Deleting a Product

1. Select the product
2. Click **"Delete"** button
3. Confirm deletion
4. **Warning:** This cannot be undone!

#### Searching Products

- Use the search box in Product Manager
- Search by name or category
- Results update in real-time

#### Managing Stock Levels

- **Low Stock Alert:** Automatically triggered at startup
- **Manual Stock Update:** Edit product and change stock quantity
- **Stock History:** View in Analytics dashboard

### 3. Customer Management

Access customer management by clicking **"👥 Customers"** in the top bar.

#### Registering a Customer

**During Sale:**
1. Click "Add Customer" button before checkout
2. Enter phone number
3. Customer automatically registered on first purchase

**Manual Registration:**
1. Open Customer Manager
2. Click "Add Customer"
3. Enter:
   - Phone number (required)
   - Name (optional)
   - Email (optional)
   - Address (optional)
4. Click "Save"

#### Viewing Customer Details

1. Open Customer Manager
2. Click on any customer
3. View:
   - Contact information
   - Total purchases (LKR)
   - Loyalty points balance
   - Purchase history (all transactions)
   - Last purchase date

#### Loyalty Points System

- **Earning:** 1 point per LKR 100 spent
- **Tracking:** Automatic during checkout
- **Viewing:** Check in Customer Manager
- **Redeeming:** (Feature coming soon)

#### Customer Search

- Search by phone number
- Search by name
- View recently active customers

### 4. Inventory Tracking

#### Stock Monitoring

**Real-Time Stock Updates:**
- Stock decreases automatically on sale
- Stock increases when editing products
- Low stock alerts when below reorder level

**Low Stock Alert:**
- Appears 2 seconds after application launch
- Shows all products below reorder level
- Dismissible dialog box

**Stock Reports:**
- Access via Reports menu
- View current stock levels
- Identify low stock items
- Export to CSV

---

## Advanced Features

### 5. Analytics Dashboard

Access analytics by clicking **"📊 Analytics"** in the top bar.

#### Sales Summary

**Today's Sales:**
- Total revenue today
- Number of transactions
- Average transaction value

**Monthly Overview:**
- Total revenue this month
- Number of sales
- Comparison with previous month

#### Top Products Analysis

- Best-selling products by revenue
- Best-selling products by quantity
- Product performance trends

#### Revenue Trends

- Daily sales trends
- Weekly comparisons
- Monthly patterns

#### Category Performance

- Revenue by category
- Top-performing categories
- Category distribution

#### Using Analytics

1. Click "📊 Analytics" button
2. View summary statistics
3. Scroll for detailed breakdowns
4. Use data for business decisions:
   - Identify best sellers
   - Plan inventory purchases
   - Optimize stock levels

### 6. Reports

Access reports by clicking **"📄 Reports"** in the top bar.

#### Available Report Types

1. **Daily Sales Report**
   - All sales for selected date
   - Items sold and quantities
   - Total revenue

2. **Monthly Sales Report**
   - Sales summary for month
   - Daily breakdown
   - Trends and totals

3. **Top Products Report**
   - Best-selling items
   - Revenue contribution
   - Quantity sold

4. **Low Stock Report**
   - Products below reorder level
   - Current stock levels
   - Recommended reorder quantities

5. **Customer Purchase History**
   - All customer transactions
   - Loyalty points earned
   - Spending patterns

6. **Profit Analysis**
   - Revenue vs. Cost
   - Profit margins
   - Category profitability

7. **Category Performance**
   - Sales by category
   - Growth trends
   - Market share

8. **Supplier Report**
   - Products by supplier
   - Purchase history
   - Performance metrics

9. **Expense Report**
   - Business expenses
   - Category breakdown
   - Monthly totals

10. **Complete Inventory Report**
    - All products and stock
    - Valuation
    - Turnover rates

#### Generating a Report

1. Click "📄 Reports" button
2. Select report type from dropdown
3. Choose date range (if applicable)
4. Click **"Generate Report"**
5. View report in dialog

#### Exporting Reports

- Click **"Export TXT"** for text format
- Click **"Export CSV"** for spreadsheet format
- Files saved in `reports/` folder
- Open with Notepad (TXT) or Excel (CSV)

### 7. Construction Estimator

Access estimator by clicking **"🏗️ Estimator"** in the top bar.

Sri Lankan construction cost calculator for hardware requirements.

#### Using the Estimator

1. Click "🏗️ Estimator" button
2. Select **Project Type:**
   - House Foundation
   - Brick Wall
   - Plastering
   - Concrete Slab
   - Tiling
   - Painting
3. Enter **Area** in square feet
4. Click **"Calculate Estimate"**

#### Understanding Results

The estimator shows:
- **Material Cost:** Raw materials needed
- **Labor Cost:** Estimated labor charges
- **Total Cost:** Combined estimate
- **Material List:** Quantities required
- **Rate Information:** Sri Lankan market rates

**Note:** Estimates are approximate and based on standard Sri Lankan construction practices.

### 8. Multi-Language Support

BuildSmartOS supports three languages:

#### Switching Languages

1. Click the **Language** dropdown in top bar
2. Select:
   - **English** - English interface
   - **සිංහල** - Sinhala interface
   - **தமிழ்** - Tamil interface
3. UI updates immediately

#### Language Features

- All buttons and labels translate
- Product names remain as entered
- Reports generated in selected language
- Invoices include language header

#### Setting Default Language

Edit `config.json`:
```json
"settings": {
  "default_language": "sinhala"  // or "tamil" or "english"
}
```

### 9. WhatsApp Integration

Send invoices directly to customers via WhatsApp.

#### Setup (First Time)

1. Ensure WhatsApp Web is logged in on your browser
2. Check "Send WhatsApp" during checkout
3. WhatsApp Web will open automatically
4. Confirm the send

#### Using WhatsApp Invoicing

1. Add customer phone number before checkout
2. Check **"Send WhatsApp"** checkbox
3. Complete checkout
4. WhatsApp Web opens with pre-filled message
5. Press Enter to send

**Message Includes:**
- Business name
- Invoice number
- Total amount
- Thank you message
- PDF invoice (if configured)

### 10. PDF Invoice Generation

Automatic professional invoices for every sale.

#### Invoice Contents

- **Header:** Business name and logo
- **Invoice Number:** Unique transaction ID
- **Date & Time:** Transaction timestamp
- **Customer Info:** Phone number (if provided)
- **Itemized List:** 
  - Product names
  - Quantities
  - Unit prices
  - Subtotals
- **Total Amount:** Grand total in LKR
- **Footer:** Thank you message

#### Accessing Invoices

- **Location:** `bills/` folder in BuildSmartOS directory
- **Filename Format:** `invoice_{transaction_id}_{timestamp}.pdf`
- **Opening:** Double-click to open with PDF reader

#### Customizing Invoices

Edit `pdf_generator.py` to customize:
- Business logo
- Header colors
- Footer text
- Font styles

---

## Daily Operations

### Opening Procedures

1. **Start Application**
   - Double-click `Run BuildSmartOS.bat`
   - Wait for window to load (2-5 seconds)

2. **Check Low Stock Alert**
   - Review low stock items
   - Plan reorder if needed
   - Dismiss alert

3. **Verify System Ready**
   - Products loaded and visible
   - Database connected
   - No error messages

### Processing Sales

**Quick Sale Workflow:**
1. Search or browse for product
2. Add to cart (+)
3. Repeat for all items
4. Add customer (optional, for loyalty points)
5. Checkout
6. Print or send invoice

**With Customer:**
1. Click "Add Customer"
2. Enter phone (e.g., 0771234567)
3. Proceed with sale
4. Loyalty points auto-added

### End-of-Day Procedures

1. **Generate Daily Sales Report**
   - Click "📄 Reports"
   - Select "Daily Sales Report"
   - Export to CSV
   - Review total revenue

2. **Check Stock Levels**
   - Generate "Low Stock Report"
   - Note items to reorder
   - Update stock if inventory done

3. **Backup Database** (Recommended)
   ```bash
   python database_setup.py
   ```
   - Creates backup in `backups/` folder
   - Filename includes timestamp

4. **Review Analytics**
   - Check today's performance
   - Compare with targets
   - Identify trends

### Stock Management Workflow

#### Receiving New Stock

1. Open Product Manager
2. Find the product
3. Click "Edit"
4. Increase stock quantity
5. Save changes

**Example:**
- Current stock: 10 bags cement
- Received: 100 bags
- New stock: 110 bags

#### Conducting Stock Count

1. Generate "Complete Inventory Report"
2. Print or export to CSV
3. Physically count items
4. Update discrepancies in Product Manager
5. Document in expense tracker (if applicable)

#### Handling Returns

1. If product unused:
   - Edit product
   - Increase stock
   - Note in comments
2. If product damaged:
   - Do not return to stock
   - Record as expense (loss)

---

## Reports & Analytics

### Understanding Key Metrics

#### Revenue Metrics

- **Daily Revenue:** Sum of all sales today
- **Monthly Revenue:** Sum of all sales this month
- **Average Transaction:** Total revenue ÷ number of sales

#### Stock Metrics

- **Stock Value:** Current stock × unit price
- **Turnover Rate:** How quickly stock sells
- **Reorder Point:** When to reorder stock

#### Customer Metrics

- **Customer Lifetime Value:** Total spent by customer
- **Loyalty Points:** Rewards earned
- **Repeat Customer Rate:** % of returning customers

### Making Data-Driven Decisions

#### Stock Optimization

**Use:** Top Products Report + Low Stock Report

**Action:**
1. Identify best sellers
2. Maintain higher stock levels
3. Reduce slow-moving items
4. Adjust reorder levels

#### Pricing Strategy

**Use:** Profit Analysis Report

**Action:**
1. Check profit margins per product
2. Adjust prices for better margins
3. Identify loss leaders
4. Plan promotions

#### Customer Retention

**Use:** Customer Purchase History

**Action:**
1. Identify top customers
2. Offer loyalty rewards
3. Engage inactive customers
4. Build relationships

---

## Tips & Best Practices

### Sales Best Practices

1. **Always Use Search:** Faster than scrolling
2. **Add Customer Info:** Build loyalty database
3. **Double-Check Cart:** Avoid mistakes before checkout
4. **Send WhatsApp Invoices:** Professional and convenient
5. **Review Daily Reports:** Track performance

### Inventory Best Practices

1. **Set Accurate Reorder Levels:** Prevent stockouts
2. **Regular Stock Counts:** Monthly recommended
3. **Update Stock Immediately:** After receiving deliveries
4. **Monitor Low Stock Alerts:** Reorder proactively
5. **Remove Discontinued Items:** Keep database clean

### Customer Management Best Practices

1. **Collect Phone Numbers:** Even for small sales
2. **Verify Phone Numbers:** Ensure accuracy
3. **Update Customer Info:** Keep records current
4. **Track Purchase History:** Understand buying patterns
5. **Use Loyalty Program:** Encourage repeat business

### System Maintenance

1. **Daily Backup:** Before closing
2. **Weekly Review:** Check analytics
3. **Monthly Cleanup:** Archive old data
4. **Update Products:** Keep prices current
5. **Test Features:** Ensure everything works

### Security Best Practices

1. **Protect Database:** `buildsmart_hardware.db` contains all data
2. **Regular Backups:** Store in multiple locations
3. **Secure Config:** Keep `config.json` safe
4. **Password Protect:** Lock computer when away
5. **Network Security:** Use firewall on computer

### Performance Optimization

1. **Close Unused Windows:** Keep only main window open
2. **Clear Old Data:** Archive transactions older than 2 years
3. **Regular Maintenance:** Run database validator monthly
4. **Limit Products:** Don't exceed 10,000 products for best performance
5. **Monitor Resources:** Check CPU/RAM usage

---

## Quick Reference

### Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Search Products | Click search box, start typing |
| Checkout | Click Checkout button |
| Clear Cart | Remove all items manually |
| Add Customer | Click Add Customer button |
| Open Products | Click 📦 Products |
| Open Customers | Click 👥 Customers |
| Open Reports | Click 📄 Reports |
| Open Analytics | Click 📊 Analytics |

### Common Tasks

| Task | Steps |
|------|-------|
| Make a sale | Search → Add to cart → Checkout |
| Add customer to sale | Add Customer → Enter phone → Checkout |
| Generate daily report | Reports → Daily Sales → Generate |
| Check low stock | Reports → Low Stock → Generate |
| Add new product | Products → Add Product → Fill form → Save |
| Update stock | Products → Edit → Change stock → Save |
| View customer history | Customers → Select customer → View history |
| Send WhatsApp invoice | Add customer → Check "Send WhatsApp" → Checkout |

### File Locations

| File/Folder | Purpose | Location |
|-------------|---------|----------|
| Database | All data | `buildsmart_hardware.db` |
| Invoices | PDF bills | `bills/` folder |
| Reports | Exported reports | `reports/` folder |
| Backups | Database backups | `backups/` folder |
| Config | Settings | `config.json` |

---

## Frequently Asked Questions

### General Questions

**Q: Can I use BuildSmartOS on multiple computers?**  
A: Yes, but you'll need to copy the database file to share data, or set up network database access.

**Q: Is internet required?**  
A: No, for core features. WhatsApp and voice commands require internet.

**Q: Can I customize the interface?**  
A: Limited customization via `config.json`. Theme and language can be changed.

### Sales Questions

**Q: What happens if I checkout without customer info?**  
A: Sale proceeds normally, but customer doesn't earn loyalty points.

**Q: Can I edit a completed sale?**  
A: No, sales are final. You can issue a refund by manually adjusting stock and recording expense.

**Q: How do I handle discounts?**  
A: Temporarily edit product price before adding to cart, or deduct from total and record in expenses.

### Product Questions

**Q: Can I import products from Excel?**  
A: Yes, use the CSV import feature in Product Manager (requires proper formatting).

**Q: What if I run out of stock during a sale?**  
A: System prevents adding more than available stock to cart.

**Q: Can I have products with same name but different sizes?**  
A: Yes, make them separate products (e.g., "Paint Red 1L" and "Paint Red 4L").

### Technical Questions

**Q: Database file is growing large, what to do?**  
A: Archive old data, run database maintenance, or contact support.

**Q: Application is slow, how to fix?**  
A: Reduce number of products displayed, close other programs, or upgrade hardware.

**Q: How to restore from backup?**  
A: Replace `buildsmart_hardware.db` with backup file from `backups/` folder.

---

## Support & Contact

### Getting Help

1. **Check Troubleshooting Guide:** `TROUBLESHOOTING.md`
2. **Review Developer Guide:** `DEVELOPER_GUIDE.md`
3. **Check Test Reports:** Verify system health

### Contact Information

- **Email:** info@buildsmart.lk
- **Phone:** 077-1234567
- **Website:** buildsmart.lk

### Reporting Issues

When reporting issues, include:
- BuildSmartOS version
- Windows version
- Error message (if any)
- Steps to reproduce
- Screenshots (if applicable)

---

**BuildSmartOS User Manual v1.0**  
*Last Updated: December 15, 2025*  
*Made with ❤️ in Sri Lanka*
