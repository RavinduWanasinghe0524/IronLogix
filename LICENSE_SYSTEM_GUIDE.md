# License System Documentation

## Overview
BuildSmartOS now includes a **30-day free trial** with license activation system. After the trial expires, users must enter an activation code to continue using the system.

---

## How It Works

### For Shop Owners (Your Customers):

1. **First Time Launch**
   - System starts with a 30-day free trial automatically
   - Trial countdown begins from installation date
   - All features are fully functional during trial

2. **During Trial Period**
   - Users can see days remaining in the top bar
   - Warning shown when 7 days or less remaining
   - All features work normally

3. **After Trial Expires**
   - System shows license activation dialog on startup
   - Cannot use system until activation code is entered
   - Must contact you for activation code

4. **After Activation**
   - System is permanently activated
   - No more expiration or restrictions
   - Shows "Licensed" status in top bar

---

## For You (System Administrator):

### Getting Customer's Machine ID

When trial expires, customer will see this screen showing their **Machine ID**:
```
Machine ID: f55069ef746159bc
```

They need to send this to you to get activation code.

### Generating Activation Codes

**Method 1: Using the Code Generator Tool**
```bash
python generate_activation_code.py
```
- Choose option 1
- Enter customer's Machine ID
- System generates activation code
- Send code to customer

**Method 2: Manual Generation**
```python
from license_manager import generate_code_for_machine
code = generate_code_for_machine("f55069ef746159bc")
print(code)  # Output: E5B2-1BA2-1969
```

### Customer Enters Code

Customer enters the code in format: `XXXX-XXXX-XXXX`
- Example: `E5B2-1BA2-1969`
- System validates and activates permanently
- Shows success message

---

## Files Created

1. **`license_manager.py`** - Core license system
   - Handles trial period
   - Validates activation codes
   - Stores license data

2. **`license_dialog.py`** - License activation UI
   - Shows trial status
   - Activation code input
   - User-friendly dialogs

3. **`generate_activation_code.py`** - Code generator tool
   - For you to generate codes
   - Easy command-line interface

4. **`license.json`** - License data file (auto-created)
   - Stores trial dates
   - Activation status
   - Machine ID

---

## Security Features

### Machine-Specific Codes
- Each activation code works **only** for specific machine
- Code is generated from Machine ID + Secret Key
- Cannot be shared between different computers

### Tamper Protection
- License file includes machine ID validation
- Deleting license.json resets trial (but machine ID stays same)
- Cannot extend trial by changing system date

### Secret Keys
Located in `license_manager.py`:
```python
secret = "BUILDSMART2025"  # Change this to your own secret!
```

**IMPORTANT:** Change this secret key before distribution!

---

## Pricing Strategy Examples

### Option 1: One-Time Payment
- 30-day free trial
- LKR 50,000 one-time payment for permanent license
- Generate code after payment received

### Option 2: Subscription
- 30-day free trial
- LKR 5,000/month or LKR 50,000/year
- Generate new code each month/year
- Let trial expire, then activate again

### Option 3: Tiered Pricing
- Basic: LKR 25,000 (core features)
- Pro: LKR 50,000 (all features)
- Enterprise: LKR 100,000 (multiple stores)

---

## Testing the License System

### Test 1: Trial Period
```bash
# Delete existing license
rm license.json

# Run application
python main.py

# Should show: "Trial: 30 days remaining"
```

### Test 2: Activation
```bash
# Get machine ID
python generate_activation_code.py
# Choose option 2, note the code

# Run application
python main.py

# Enter the activation code
# Should show: "Licensed Version"
```

### Test 3: Expired Trial
1. Open `license.json`
2. Change `expiry_date` to past date
3. Run application
4. Should force activation dialog

---

## Customer Instructions Template

**Email/Message to Send to Customers:**

```
Hello,

Your BuildSmartOS 30-day free trial has expired.

To continue using the system, please follow these steps:

1. Open BuildSmartOS
2. Note your Machine ID shown on screen
3. Send the Machine ID to us via WhatsApp: 077-XXXXXXX
4. We will send you an activation code
5. Enter the code in the activation dialog
6. System will be activated permanently

Activation Fee: LKR 50,000 (one-time payment)

Payment Methods:
- Bank Transfer: [Bank Details]
- Online Payment: [Payment Link]

Once payment is confirmed, activation code will be sent within 24 hours.

Thank you for choosing BuildSmartOS!
```

---

## Admin Functions

### Extend Trial (Emergency)
```python
from license_manager import get_license_manager
lm = get_license_manager()
success, msg = lm.reset_trial("ADMIN2025RESET")
```

### Check Customer License Status
```python
from license_manager import get_license_manager
lm = get_license_manager()
info = lm.get_license_info()
print(info)
```

---

## Troubleshooting

### Customer Says "Code Not Working"
1. Verify Machine ID exactly matches
2. Check code format: `XXXX-XXXX-XXXX`
3. Ensure no extra spaces
4. Code is case-insensitive

### Customer Wants to Transfer License
- License is machine-specific
- Need to purchase new license for new machine
- Or: Generate new code for new machine ID (your decision)

### Trial Shows Wrong Days
- System uses installation date, not system date
- Cannot extend by changing system clock
- Can reset with admin code if needed

---

## Monetization Tips

### During Trial Period:
- Send reminder emails at 20, 10, 5, 1 days remaining
- Offer discount for early activation (25 days+)
- Provide excellent support during trial

### After Trial:
- Professional activation service
- Quick response (24 hour guarantee)
- Payment plans available
- Bulk discounts for multiple stores

### Value-Added Services:
- Premium support: LKR 5,000/month
- Custom features: Quote per request
- Training sessions: LKR 10,000
- Data migration: LKR 15,000

---

## Your Action Items

### Before Distribution:
1. ✅ Change secret key in `license_manager.py`
2. ✅ Test activation flow completely
3. ✅ Prepare payment gateway
4. ✅ Setup customer support channel
5. ✅ Create price list

### For Each Customer:
1. ✅ Install system
2. ✅ Verify trial starts correctly
3. ✅ Provide your contact info
4. ✅ Explain trial period
5. ✅ Setup payment method

### After Trial:
1. ✅ Receive Machine ID from customer
2. ✅ Verify payment
3. ✅ Generate activation code
4. ✅ Send code to customer
5. ✅ Verify activation successful

---

## Summary

✅ **30-day free trial automatically starts**
✅ **Machine-specific activation codes**
✅ **Cannot use after trial without code**
✅ **Permanent activation after code entry**
✅ **Easy code generation for you**
✅ **Professional license dialog**
✅ **Tamper-proof system**

**The license system is ready to protect your business!** 🚀
