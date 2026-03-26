# AfriBazaar – Payment & Currency System
**Module Owner:** NOUDOU  
**Branch:** `payment-system`  
**App folder:** `ecommerce/afribazaar/payments/`

---

## What This Module Does

This app implements the full **Payment & Currency System** for AfriBazaar.  
It covers everything described in the project specification:

| Feature | Status |
|---|---|
| Multi-currency display (USD, EUR, XAF, NGN, GHS, KES, ZAR…) | ✅ |
| Live exchange rates stored in the database | ✅ |
| Currency selector in the navbar (session-based) | ✅ |
| Payment page (card, mobile money, bank transfer, cash on delivery) | ✅ |
| Payment confirmation page | ✅ |
| Payment failed page | ✅ |
| Live currency converter widget | ✅ |
| Currency rates public page | ✅ |
| JSON API endpoint for currency conversion | ✅ |
| Admin panel integration | ✅ |
| Unit tests | ✅ |
| Seed data for currencies & rates | ✅ |

---

## File Map

```
payments/
├── __init__.py
├── apps.py                  ← App config (name="payments")
├── models.py                ← Currency, ExchangeRate, Payment, Transaction
├── views.py                 ← All 6 views
├── urls.py                  ← URL routes (namespace="payments")
├── forms.py                 ← PaymentForm, CurrencySelectForm
├── admin.py                 ← Admin registrations
├── utils.py                 ← convert_to_usd(), convert_from_usd(), etc.
├── tests.py                 ← Unit + view tests
├── migrations/
│   ├── __init__.py
│   └── 0001_initial.py      ← Creates all 4 tables
├── fixtures/
│   └── currencies_seed.json ← 10 currencies + exchange rates
└── templatetags/
    ├── __init__.py
    └── payment_tags.py      ← {% convert_price %} filter + {% currency_selector_html %}

templates/payments/
├── payment_page.html        ← Main payment form
├── payment_confirmation.html
├── payment_failed.html
└── currency_rates.html      ← Public rates page + converter widget
```

---

## URL Routes

All routes are prefixed with `/payments/` (configured in root `urls.py`).

| URL | View | Name |
|---|---|---|
| `/payments/pay/` | `payment_page` | `payments:payment_page` |
| `/payments/confirmation/` | `payment_confirmation` | `payments:payment_confirmation` |
| `/payments/failed/` | `payment_failed` | `payments:payment_failed` |
| `/payments/currencies/` | `currency_rates` | `payments:currency_rates` |
| `/payments/set-currency/` | `set_currency` | `payments:set_currency` |
| `/payments/api/convert/` | `api_convert` | `payments:api_convert` |

---

## Setup Instructions (for teammates pulling this branch)

### 1. Run migrations
```bash
cd ecommerce/afribazaar
python manage.py migrate
```

### 2. Load seed data (currencies + exchange rates)
```bash
python manage.py loaddata payments/fixtures/currencies_seed.json
```

### 3. Run the dev server
```bash
python manage.py runserver
```

### 4. Visit the pages
- Home with currency selector: http://127.0.0.1:8000/
- Payment form: http://127.0.0.1:8000/payments/pay/
- Currency rates: http://127.0.0.1:8000/payments/currencies/
- Admin panel: http://127.0.0.1:8000/admin/

### 5. Run tests
```bash
python manage.py test payments
```

---

## How to Integrate With Other Modules

### Randy (Cart & Order) → Payments
When an order is created and ready for payment, set these two session keys
before redirecting the customer to `/payments/pay/`:

```python
# In Randy's checkout view, after creating the order:
request.session["pending_order_id"]  = order.id
request.session["order_amount_usd"]  = float(order.total_amount)
return redirect("payments:payment_page")
```

The payment module will pick these up automatically.

### Finamou (Products) – Show prices in chosen currency
Load the custom template tag in any product template:

```django
{% load payment_tags %}

<!-- Convert a USD price to the visitor's selected currency -->
{{ product.base_price|convert_price:request.session.selected_currency }}

<!-- Or embed the currency selector widget anywhere -->
{% currency_selector_html %}
```

### Rejoice (Users/Auth) – No changes needed
The payment module stores `order_id` as a plain integer.
No FK relationship to the User model is required from this module.

---

## Database Models (summary)

```
Currency          → currency_code (PK), currency_name, symbol, is_active
ExchangeRate      → id, currency (FK), rate_to_usd, date_updated
Payment           → id, order_id, currency (FK), amount_in_currency,
                    amount_in_usd, payment_method, payment_status,
                    created_at, updated_at, reference_number
Transaction       → id, payment (FK), event_type, transaction_date, notes
```

---

## Notes for the Team
- **Do not modify** `afribazaar/settings.py` or `afribazaar/urls.py` beyond the
  two lines already added for this module.
- All payments templates are in `templates/payments/` — they will not conflict
  with templates from other modules.
- Exchange rates in the seed file are **approximate** values for demo purposes.
  In production these would be updated via an external API (e.g. Open Exchange Rates).
