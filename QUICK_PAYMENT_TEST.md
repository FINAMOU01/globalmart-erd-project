# 🎯 Payment Form Testing Guide

## ✅ Server Status

**Server**: Running at `http://localhost:8000/`

---

## 🔗 Testing the Payment Form

### Step 1: Open Payment Page
```
http://localhost:8000/payments/pay/
```

### Step 2: Test Payment Method Changes ✓

**Test A - Credit Card** (Default)
- Observe the form shows:
  - ✓ Cardholder Name field
  - ✓ Last 4 digits field
- Button says: "Process Card Payment"

**Test B - Switch to Mobile Money**
- Click "Mobile Money" radio button
- Observe the form CHANGES:
  - ✗ Cardholder Name field → DISAPPEARS
  - ✗ Last 4 digits field → DISAPPEARS
  - ✓ Mobile Number field → APPEARS
- Button now says: "Send Mobile Money"

**Test C - Switch to Bank Transfer**
- Click "Bank Transfer" radio button
- Form changes:
  - ✗ Payment method fields → DISAPPEAR
  - ✓ Bank details info box → APPEARS
- Button says: "Confirm Transfer"

**Test D - Switch to Cash on Delivery**
- Click "Cash on Delivery" radio button
- Form changes:
  - ✗ All payment fields → DISAPPEAR
  - ✓ COD info box → APPEARS
- Button says: "Place Order (Pay on Delivery)"

### Step 3: Test Currency Conversion ✓

**Test A - Default USD**
- Page loads with: **$ 95.00**
- Order summary shows: **$ 95.00**
- Conversion rate: **1.0000**

**Test B - Change to EUR (Euro)**
- Open dropdown: "Pay in"
- Select: **EUR (€)**
- Wait 1-2 seconds for conversion
- Amount should change to: **€ 102.60** (approximately)
- Symbol changes: $ → €
- Rate shows: ~1.08

**Test C - Change to NGN (Nigerian Naira)**
- Select: **NGN (₦)**
- Wait for conversion
- Amount should change to: **₦ 146,154.00** (approximately)
- Symbol: ₦
- Rate: ~1,538.46

**Test D - Change to XAF (CFA Franc)**
- Select: **XAF (FCFA)**
- Amount should change to: **FCFA 57,575.00** (approximately)
- Symbol: FCFA
- Rate: ~606.06

**Test E - Change to ZAR (South African Rand)**
- Select: **ZAR (R)**
- Amount should change to: **R 1,762.50** (approximately)
- Symbol: R
- Rate: ~18.55

---

## 🔍 Debugging - Open DevTools (F12)

### Console Tab
Look for green ✓ messages like:
```
Payment form script loading...
Elements loaded: {currencySelect: true, displayAmount: true, ...}
Currency selected: EUR
Loading rate for currency: EUR
Fetching API: /payments/api/convert/?from=USD&to=EUR&amount=95
API Response: {success: true, amount: 102.60, rate: 1.08, symbol: "€", ...}
Updating display: {...}
✓ Display updated
```

### Network Tab
- Look for requests to: `/payments/api/convert/?from=USD&to=...`
- Response should be JSON with: `success`, `amount`, `rate`, `symbol`

### Expected API Response Example
```json
{
  "success": true,
  "amount": 102.6,
  "rate": 1.08,
  "symbol": "€",
  "currency_code": "EUR",
  "formatted": "€ 102.60"
}
```

---

## 📋 Full Test Checklist

### Payment Method Toggle ✓
- [ ] Card method selected by default
  - [ ] Shows cardholder name field
  - [ ] Shows last 4 digits field
- [ ] Mobile Money selected
  - [ ] Cardholder/last 4 fields disappear
  - [ ] Mobile number field appears
- [ ] Bank Transfer selected
  - [ ] All fields disappear
  - [ ] Bank details info displays
- [ ] Cash on Delivery selected
  - [ ] All fields disappear
  - [ ] COD info displays
- [ ] Button label changes for each method

### Currency Conversion ✓
- [ ] USD: $ 95.00
- [ ] EUR: € 102.60 (approximately)
- [ ] NGN: ₦ 146,154.00 (approximately)
- [ ] XAF: FCFA 57,575.00 (approximately)
- [ ] ZAR: R 1,762.50 (approximately)
- [ ] GHS: ₵ 1,181.25 (approximately)
- [ ] GBP: £ 74.80 (approximately)
- [ ] KES: KSh 12,272.50 (approximately)
- [ ] EGP: E£ 2,926.50 (approximately)
- [ ] MAD: د.م. 968.00 (approximately)

### Order Summary Updates ✓
- [ ] Total updates when currency changes
- [ ] Symbol updates when currency changes
- [ ] Exchange rate displays below order summary

### Form Interaction ✓
- [ ] Switching between payment methods works smoothly
- [ ] Switching currencies updates instantly
- [ ] No console errors (F12 → Console tab)
- [ ] All conversion rates look reasonable

---

## 🚨 Troubleshooting

### Problem: Form doesn't change when I select payment method
**Solution**:
- Open DevTools (F12) → Console tab
- You should see: "Showing payment fields for method: CARD"
- If no logs, try refreshing the page
- Check that radio button actually changes color/style

### Problem: Currency doesn't convert
**Solution**:
- Check Network tab (F12) for API calls to `/payments/api/convert/`
- If API returns error, check console for error message
- Verify server is still running (http://localhost:8000/ should load)
- Try a full page refresh (Ctrl+F5)

### Problem: Amount shows 95.00 for all currencies
**Solution**:
- This means conversion rate isn't loading
- Check DevTools Console for errors
- Verify API response includes `rate` field
- Try changing currency again or refreshing

### Problem: Server not responding
**Solution**:
- Check if Terminal 6ed6b8cb... is still running
- You should see "Starting development server at http://127.0.0.1:8000/"
- If not, restart with:
  ```powershell
  cd c:\Users\finamou\Desktop\globalmart-erd-project\ecommerce\afribazaar
  python manage.py runserver
  ```

---

## 💡 Quick API Test (PowerShell)

Run from a new PowerShell window while server is running:

```powershell
cd c:\Users\finamou\Desktop\globalmart-erd-project\ecommerce\afribazaar
.\test_api_live.ps1
```

This will test API conversions directly.

---

## ✅ Success Criteria

Everything working correctly when:

1. ✓ Selecting different payment methods shows/hides correct fields
2. ✓ Selecting different currencies converts amounts accurately
3. ✓ Button labels change based on payment method
4. ✓ Order summary updates with new amounts/symbols
5. ✓ No console errors in DevTools
6. ✓ API responses include rate, symbol, and currency_code

---

## 📝 Notes

- **Field visibility**: Uses CSS class `d-none` (Bootstrap display:none)
- **Amount conversion**: Uses JavaScript `(ORDER_AMOUNT_USD * rate).toFixed(2)`
- **API calls**: Async fetch to `/payments/api/convert/` endpoint
- **Supported currencies**: 10 total across Africa, Europe, and Middle East

---

## 🎉 Ready to Test!

Open http://localhost:8000/payments/pay/ and start testing!

Questions? Check console logs (F12) for detailed debugging information.

---

**Commit**: dcbd2be "fix: Complete payment form functionality - methods & currency conversion"
**Branch**: test-currency → main (pushed to GitHub)
