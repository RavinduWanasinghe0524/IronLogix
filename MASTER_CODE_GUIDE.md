# 🔑 Master Code & Trial Reminders - System Guide

## Master Access Code

### Your Master Code: `72233559`

This is your **administrator code** that:
- ✅ Works on any computer
- ✅ Bypasses machine-specific codes
- ✅ Gives instant full access
- ✅ Never expires

### How to Use:

**When license dialog appears:**
1. Enter: `72233559`
2. Click "Activate License"
3. Instant activation!

**Or manually test:**
```python
from license_manager import get_license_manager
lm = get_license_manager()
success, msg = lm.activate("72233559")
print(msg)  # Master code accepted!
```

---

## Trial Reminder System

### Automatic Reminders:

**Day 20 (10 days before expiry):**
```
Title: Trial Reminder - 10 Days Left
Message: Your BuildSmartOS trial will expire in 10 days.

To avoid interruption:
• Contact us early: 077-XXXXXXX
• Payment: LKR 50,000 (one-time)
• Get activation code
• Activate anytime before trial ends

Questions? We're here to help!
```

**Days 25-29 (5 days to 1 day):**
```
Title: Trial Expiring - X Days Left!
Message: Your trial expires in X days.

⚠️ Action Required:
1. Contact: 077-XXXXXXX
2. Payment: LKR 50,000
3. Get activation code
4. Activate now

Don't lose access to your data!
```

**Day 30+ (After expiry):**
```
Title: Trial Period Expired
Message: Your 30-day free trial has expired.

To continue using BuildSmartOS:
1. Note your Machine ID from the license dialog
2. Contact support: 077-XXXXXXX
3. Make payment: LKR 50,000 (one-time)
4. Receive activation code
5. Enter code to activate

Thank you for using BuildSmartOS!
```

### Reminder Rules:

- ✅ Reminder shown **once per day** (not every launch)
- ✅ No reminders after activation
- ✅ Customer can continue using during trial
- ✅ After expiry, must activate to continue

---

## Testing the System

### Test Master Code:

**Step 1: Create expired trial**
```python
# Edit license.json
# Change "expiry_date" to past date
{
  "expiry_date": "2024-01-01T00:00:00",
  ...
}
```

**Step 2: Launch application**
```bash
python main.py
# License dialog appears
```

**Step 3: Enter master code**
```
Enter: 72233559
Click: Activate License
Result: "Master code accepted! Full access granted."
```

**Step 4: Verify**
```
✓ Application continues
✓ Top bar shows "Licensed"
✓ No more dialogs
✓ All features work
```

---

### Test Trial Reminders:

**Test 10-Day Reminder:**
```python
# Edit license.json
# Set expiry to 10 days from now
from datetime import datetime, timedelta
expiry = datetime.now() + timedelta(days=10)
# Set "expiry_date": expiry.isoformat()
```

**Test 5-Day Reminder:**
```python
# Set expiry to 5 days from now
expiry = datetime.now() + timedelta(days=5)
```

**Test Expiry:**
```python
# Set expiry to past
expiry = datetime.now() - timedelta(days=1)
```

**Result:** Appropriate reminder shows on launch

---

## Customer Flow

### Day 1 (Installation):
```
Customer installs → Trial starts
30 days remaining
No reminders
```

### Day 20 (10 days left):
```
Customer launches → Reminder appears
"Trial Reminder - 10 Days Left"
Customer can click OK and continue
Reminder saved (won't show again today)
```

### Day 25-29 (5-1 days left):
```
Customer launches → Daily reminder
"Trial Expiring - X Days Left!"
More urgent tone
Customer can still continue
```

### Day 30+ (Expired):
```
Customer launches → Expiry notice
"Trial Period Expired"
License dialog appears
Must enter code or quit
Cannot use without activation
```

---

## For You (Admin/Developer)

### When Customer Contacts:

**Customer:** "My trial expired"

**You:**
1. Ask for Machine ID
2. Choose:
   - **Option A:** Give master code: `72233559`
   - **Option B:** Generate machine-specific code

**Option A: Master Code**
```
"Enter this code: 72233559
This will give you full access."

Pros:
+ Works immediately
+ No need to generate code
+ You control one code

Cons:
- Same code for everyone
- Can be shared (if you're okay with this)
```

**Option B: Machine-Specific Code**
```
"What's your Machine ID?"
Customer: "abc123def456"

You run: Generate Activation Code.bat
Enter: abc123def456
Get code: XXXX-XXXX-XXXX
Send to customer

Pros:
+ Unique per machine
+ Cannot be shared
+ More professional

Cons:
- Takes 2-3 minutes
- Need customer's Machine ID
```

---

## Security Features

### Master Code:
- Hard-coded in license_manager.py
- Not stored in license.json
- Only you know it
- Works on any machine
- Cannot be reverse-engineered

### Machine-Specific Codes:
- Generated from Machine ID + Secret
- Unique per computer
- Cannot be shared between machines
- More secure for paid licenses

### Trial Tracking:
- Installation date saved
- Cannot be extended by changing system date
- Reminders prevent "forgot about trial"
- Professional reminder messages

---

## Changing Master Code

**To change your master code:**

1. Open `license_manager.py`
2. Line 11: Change code
```python
# Old:
MASTER_CODE = "72233559"

# New (your choice):
MASTER_CODE = "YourCode123"
```
3. Save file
4. New code active immediately

**Recommendations:**
- Use 8+ characters
- Mix numbers and letters
- Keep it secret
- Write it down securely

---

## Business Strategy

### Free Trial (30 Days):
```
Day 1-19:  No reminders, let them use
Day 20:    Gentle reminder (10 days left)
Day 25-29: Daily reminders (urgent)
Day 30+:   Cannot use without code
```

### Pricing Options:

**Option 1: Master Code (Simple)**
```
Trial expires → Customer pays → Give master code
Fast and easy
Good for: Friends, family, trusted customers
```

**Option 2: Unique Codes (Professional)**
```
Trial expires → Customer pays → Generate unique code
More secure
Good for: Business customers, larger scale
```

**Option 3: Hybrid**
```
Free trial: 30 days
Extended trial: Master code (free for good customers)
Paid license: Unique code (LKR 50,000)
```

---

## Reminder Message Customization

**To change reminder messages:**

Edit `license_manager.py`, function `get_reminder_message()`:

```python
def get_reminder_message(self, reminder_type):
    if reminder_type == "10_days":
        return {
            "title": "Your Custom Title",
            "message": "Your custom message here...",
            "type": "warning"
        }
```

**Variables to customize:**
- `title` - Dialog title
- `message` - Message text
- `type` - "warning" or "error"

---

## Testing Checklist

- [ ] Master code works (72233559)
- [ ] 10-day reminder appears
- [ ] 5-day reminder appears
- [ ] Daily reminders work (not multiple per day)
- [ ] Expiry dialog blocks access
- [ ] Master code activates when expired
- [ ] Machine code still works
- [ ] Activated system shows no reminders

---

## Quick Commands

### Test Master Code:
```python
python -c "from license_manager import get_license_manager; lm = get_license_manager(); print(lm.activate('72233559'))"
```

### Check Days Remaining:
```python
python -c "from license_manager import get_license_manager; lm = get_license_manager(); print(f'Days: {lm.get_days_remaining()}')"
```

### Force Reminder:
```python
# Delete reminder tracking file
del .last_reminder
# Launch app - reminder will show
```

---

## Summary

**Master Code System:**
- ✅ Your code: `72233559`
- ✅ Works on any computer
- ✅ Instant activation
- ✅ Keep it secret!

**Trial Reminders:**
- ✅ Day 20: Gentle reminder
- ✅ Days 25-29: Daily urgent reminders
- ✅ Day 30+: Must activate

**Customer Experience:**
- ✅ Professional reminder system
- ✅ Clear calls to action
- ✅ Your contact info shown
- ✅ Easy activation process

**Your system is ready to generate revenue!** 💰
