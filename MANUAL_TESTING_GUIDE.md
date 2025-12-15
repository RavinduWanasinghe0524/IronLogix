# BuildSmartOS - Manual Testing Guide

## Overview

This guide helps you manually test the BuildSmartOS application to verify UI/UX functionality and visual elements that cannot be tested automatically.

---

## Prerequisites

1. Ensure all automated tests have passed
2. Database has test data (run `generate_test_data.py` if needed)
3. Close any running instances of BuildSmartOS

---

## Test 1: Application Launch

### Steps:
1. Run application:
   ```bash
   python main.py
   ```
   OR double-click: `Run BuildSmartOS.bat`

### Expected Results:
- ✅ Application window opens (1400x900)
- ✅ Dark theme applied
- ✅ Top bar with all buttons visible
- ✅ Product list on left side
- ✅ Cart panel on right side
- ✅ No error messages in console
- ✅ Products load and display

### Pass Criteria:
All elements render correctly without errors

---

## Test 2: Language Switching

### Steps:
1. Click language dropdown (top bar)
2. Select "Sinhala"
3. Observe UI changes
4. Select "Tamil"
5. Observe UI changes
6. Select "English"

### Expected Results:
- ✅ UI labels update to selected language
- ✅ Button text changes
- ✅ No broken Unicode characters
- ✅ All text readable
- ✅ No layout issues

### Pass Criteria:
All three languages display correctly

---

## Test 3: Product Search

### Steps:
1. Click in search box
2. Type "cement"
3. Observe product list filters
4. Clear search
5. Type "paint"
6. Verify filtering

### Expected Results:
- ✅ Products filter in real-time
- ✅ Only matching products shown
- ✅ Categories still grouped
- ✅ Clear search restores all products

### Pass Criteria:
Search filters products correctly

---

## Test 4: Add to Cart

### Steps:
1. Find a product with stock
2. Click the "+" button
3. Verify item appears in cart
4. Click "+" again
5. Verify quantity increases

### Expected Results:
- ✅ Item appears in cart panel
- ✅ Quantity shows correctly
- ✅ Subtotal calculated
- ✅ Total updates
- ✅ Remove (✖) button appears

### Pass Criteria:
Cart updates correctly

---

## Test 5: Cart Management

### Steps:
1. Add multiple products to cart
2. Click "✖" to remove one item
3. Add items until stock limit
4. Try adding beyond stock

### Expected Results:
- ✅ Items appear in cart list
- ✅ Remove button works
- ✅ Stock limit warning appears
- ✅ Total calculates correctly
- ✅ Cart scrolls if many items

### Pass Criteria:
All cart operations work

---

## Test 6: Customer Information

### Steps:
1. Click "Add Customer" button
2. Enter phone number (e.g., 0771234567)
3. Click OK
4. Verify customer button updates

### Expected Results:
- ✅ Dialog appears
- ✅ Can enter phone number
- ✅ Button shows phone after adding
- ✅ Loyalty points estimate appears

### Pass Criteria:
Customer info captured

---

## Test 7: Checkout Process

### Steps:
1. Add items to cart
2. Add customer (optional)
3. Check "Send WhatsApp" (optional)
4. Click "CHECKOUT" button
5. Observe success message

### Expected Results:
- ✅ Success dialog appears
- ✅ PDF path shown
- ✅ Cart clears
- ✅ Stock updated
- ✅ Customer info clears
- ✅ Points added (if customer)

### Pass Criteria:
Transaction completes successfully

---

## Test 8: PDF Invoice

### Steps:
1. Complete a checkout
2. Navigate to `bills/` folder
3. Find latest PDF
4. Open PDF invoice

### Expected Results:
- ✅ PDF file created
- ✅ File named with transaction ID
- ✅ Invoice contains:
  - Business details
  - Transaction date/time
  - Items purchased
  - Quantities and prices
  - Total amount
- ✅ Professional formatting

### Pass Criteria:
PDF generates correctly

---

## Test 9: Product Manager

### Steps:
1. Click "📦 Products" button (top bar)
2. Browse product list
3. Click "Add Product"
4. Fill in details and save
5. Edit a product
6. Delete test product

### Expected Results:
- ✅ Product manager window opens
- ✅ All products listed
- ✅ Add form works
- ✅ Edit updates product
- ✅ Delete removes product
- ✅ Search works

### Pass Criteria:
Product management fully functional

---

## Test 10: Customer Manager

### Steps:
1. Click "👥 Customers" button
2. View customer list
3. Click on a customer
4. View purchase history
5. Check loyalty points

### Expected Results:
- ✅ Customer list displays
- ✅ Purchase history shows
- ✅ Loyalty points visible
- ✅ Total purchases correct
- ✅ Can view details

### Pass Criteria:
Customer data accessible

---

## Test 11: Reports

### Steps:
1. Click "📄 Reports" button
2. Select "Daily Sales Report"
3. Generate report
4. Try "Top Products Report"
5. Export a report

### Expected Results:
- ✅ Report window opens
- ✅ Report types selectable
- ✅ Reports generate with data
- ✅ Export works (TXT/CSV)
- ✅ Data accurate

### Pass Criteria:
All report types work

---

## Test 12: Analytics Dashboard

### Steps:
1. Click "📊 Analytics" button
2. View sales summary
3. Check today's sales
4. View monthly total
5. Check top products

### Expected Results:
- ✅ Analytics dialog displays
- ✅ Today's sales shown
- ✅ Monthly total correct
- ✅ Top products listed
- ✅ Transaction count accurate
- ✅ Average transaction shown

### Pass Criteria:
Analytics display correctly

---

## Test 13: Construction Estimator

### Steps:
1. Click "🏗️ Estimator" button
2. Select project type
3. Enter area (e.g., 1000 sqft)
4. Click "Calculate"
5. View estimate

### Expected Results:
- ✅ Estimator window opens
- ✅ Project types selectable
- ✅ Area input accepts numbers
- ✅ Calculation works
- ✅ Material cost shown
- ✅ Labor cost shown
- ✅ Total displayed

### Pass Criteria:
Estimator calculates correctly

---

## Test 14: Low Stock Alerts

### Steps:
1. Launch application
2. Wait 2 seconds
3. Check for low stock warning

### Expected Results:
- ✅ Warning appears if stock low
- ✅ Lists low-stock items
- ✅ Dismissible dialog

### Pass Criteria:
Alert system functional (if applicable)

---

## Test 15: UI Responsiveness

### Steps:
1. Resize window (drag edges)
2. Minimize and restore
3. Add many items to cart
4. Load many products
5. Switch views quickly

### Expected Results:
- ✅ UI adapts to window size
- ✅ No freezing
- ✅ Smooth scrolling
- ✅ Quick response times (< 1 sec)
- ✅ No visual glitches

### Pass Criteria:
Application remains responsive

---

## Test 16: Error Handling

### Steps:
1. Try checkout with empty cart
2. Add customer with invalid phone
3. Try adding negative stock
4. Search for non-existent product

### Expected Results:
- ✅ Appropriate error messages
- ✅ No application crashes
- ✅ User-friendly messages
- ✅ Can recover from errors

### Pass Criteria:
Errors handled gracefully

---

## Test 17: Data Persistence

### Steps:
1. Add products to cart
2. Close application
3. Reopen application
4. Check products exist
5. Verify last transaction recorded

### Expected Results:
- ✅ Products still in database
- ✅ Transactions saved
- ✅ Stock levels correct
- ✅ No data loss

### Pass Criteria:
Data persists correctly

---

## Manual Testing Checklist

### Visual Elements
- [ ] All buttons clickable
- [ ] Text readable
- [ ] Colors appropriate
- [ ] Icons display
- [ ] Layouts aligned
- [ ] No overlapping elements

### Functionality
- [ ] All menus work
- [ ] All dialogs open/close
- [ ] All forms accept input
- [ ] All calculations correct
- [ ] All searches work
- [ ] All reports generate

### Performance
- [ ] Startup < 5 seconds
- [ ] Actions < 1 second response
- [ ] Smooth scrolling
- [ ] No memory leaks
- [ ] No crashes

### User Experience
- [ ] Intuitive navigation
- [ ] Clear error messages
- [ ] Helpful tooltips
- [ ] Logical workflow
- [ ] Professional appearance

---

## Test Results Template

```
Date: ______________
Tester: ______________

Test 1: Application Launch         [ ] Pass  [ ] Fail
Test 2: Language Switching          [ ] Pass  [ ] Fail
Test 3: Product Search              [ ] Pass  [ ] Fail
Test 4: Add to Cart                 [ ] Pass  [ ] Fail
Test 5: Cart Management             [ ] Pass  [ ] Fail
Test 6: Customer Information        [ ] Pass  [ ] Fail
Test 7: Checkout Process            [ ] Pass  [ ] Fail
Test 8: PDF Invoice                 [ ] Pass  [ ] Fail
Test 9: Product Manager             [ ] Pass  [ ] Fail
Test 10: Customer Manager           [ ] Pass  [ ] Fail
Test 11: Reports                    [ ] Pass  [ ] Fail
Test 12: Analytics Dashboard        [ ] Pass  [ ] Fail
Test 13: Construction Estimator     [ ] Pass  [ ] Fail
Test 14: Low Stock Alerts           [ ] Pass  [ ] Fail
Test 15: UI Responsiveness          [ ] Pass  [ ] Fail
Test 16: Error Handling             [ ] Pass  [ ] Fail
Test 17: Data Persistence           [ ] Pass  [ ] Fail

Overall Result: [ ] All Pass  [ ] Some Failures

Notes:
_________________________________________________
_________________________________________________
_________________________________________________

Signature: ______________
```

---

## Issues Found Template

```
Issue #: ____
Test: ___________
Severity: [ ] Critical  [ ] Major  [ ] Minor
Description:


Steps to Reproduce:
1.
2.
3.

Expected Result:


Actual Result:


Screenshot: (attach if applicable)
```

---

**Ready for Manual Testing!**  
Work through each test systematically and document your findings.
