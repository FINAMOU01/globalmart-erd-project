# AfriBazaar Payment System - Testing Guide

## Configuration Complete ✓

### Installed Packages:
- django-crispy-forms==2.3
- crispy-bootstrap5==2.0.2

### Settings Updated:
- Added 'crispy_forms' and 'crispy_bootstrap5' to INSTALLED_APPS
- Set CRISPY_TEMPLATE_PACK = "bootstrap5"

### Payment Form Improvements:
The PaymentForm now uses Crispy Forms with professional layout:
- Organized fieldsets with visual separators
- Responsive grid layout for card fields
- Enhanced payment method radio buttons
- Conditional display of method-specific fields
- Professional styling with gradient headers
- Dynamic amount display with currency conversion

### New Payment Template:
- Location: `templates/payments/payment_form.html`
- Uses Crispy Forms rendering with `{% crispy form %}`
- Responsive design with Bootstrap 5
- Order summary sidebar (sticky on desktop)
- Real-time currency conversion via API
- Professional gradient styling
- Security badge and SSL encryption notice

## Testing the Payment System

### 1. Start the Development Server:
```bash
cd c:\Users\finamou\Desktop\globalmart-erd-project\ecommerce\afribazaar
python manage.py runserver
```

### 2. Access the Payment Page:
Navigate to: `http://localhost:8000/payments/pay/`

### 3. Test Scenarios:

#### Scenario 1: Card Payment
1. Select USD currency
2. Choose "Credit/Debit Card" method
3. Enter cardholder name: "John Doe"
4. Enter last 4 digits: "4242"
5. Click "Process Card Payment"
6. Expected: Payment marked as SUCCESS, redirect to confirmation page

#### Scenario 2: Mobile Money
1. Select a currency (e.g., EUR, NGN)
2. Choose "Mobile Money" method
3. Enter mobile number with country code
4. Click "Send Mobile Money"
5. Expected: Payment marked as SUCCESS, redirect to confirmation page

#### Scenario 3: Cash on Delivery
1. Any currency
2. Choose "Cash on Delivery" method
3. Click "Place Order (Pay on Delivery)"
4. Expected: Payment marked as SUCCESS with COD reference

#### Scenario 4: Bank Transfer
1. Select currency
2. Choose "Bank Transfer" method
3. View bank details displayed
4. Click button
5. Expected: Payment stays PENDING, shows confirmation with bank info

### 4. Verify Database:
```bash
python manage.py shell
```

Run in shell:
```python
from payments.models import Payment, Transaction

# Check all payments
for p in Payment.objects.all():
    print(f"Payment #{p.id}: {p.amount_in_currency} {p.currency.currency_code} via {p.payment_method} - {p.payment_status}")
    
# Check transactions
for t in Transaction.objects.all():
    print(f"  → {t.event_type}: {t.notes}")
```

## Troubleshooting

### Issue: Form not rendering
- Check that load_crispy_forms_tags is present in template
- Verify INSTALLED_APPS includes 'crispy_bootstrap5'

### Issue: Styling looks off
- Clear browser cache (Ctrl+Shift+Del)
- Check Bootstrap 5 CSS is loading from CDN

### Issue: Currency conversion not working
- Check payments:api_convert endpoint is properly configured
- Verify currency data exists in database
- Check browser console for JavaScript errors

## Production Deployment

Before deploying to Render:
1. Collect static files: `python manage.py collectstatic --noinput`
2. Test in production mode: `DEBUG=False python manage.py runserver`
3. Verify Crispy Forms styling renders correctly
4. Test payment flow end-to-end
5. Check database migrations are applied

## Next Steps

- Integrate with real payment gateway (Stripe, Paystack, Flutterwave)
- Add email notifications on payment success/failure
- Implement admin dashboard to manage payments
- Add refund functionality
- Create payment history page for customers
