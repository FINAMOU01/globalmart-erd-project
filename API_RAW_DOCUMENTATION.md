# Database-First REST API Documentation
## Raw SQL Schema API for Academic Evaluation

---

## 📋 Overview

This is a **database-first REST API** that directly exposes the raw PostgreSQL schema without any business logic. It's designed to meet academic requirements for database systems coursework.

### Two APIs Coexist:
1. **Business Logic API** (`/api/`) - Complex features, nested relationships, custom logic
2. **Raw SQL API** (`/api/raw/`) - Direct schema exposure, flat JSON, no modifications

---

## 🗂️ Architecture

### Database-First Design

```
PostgreSQL Database (Neon)
        ↓
    SQL Tables (already created via script)
        ↓
    Django Models (managed=False)
        ↓
    ModelSerializers (flat, all fields)
        ↓
    ReadOnlyViewSets
        ↓
    REST Endpoints
```

### Key Design Principles

- **No Migrations**: Models use `managed=False` to prevent Django from managing tables
- **Read-Only Access**: All endpoints are GET-only via `ReadOnlyModelViewSet`
- **Flat JSON**: No nested serializers - returns database structure directly
- **No Business Logic**: Pure data exposure with pagination, search, and ordering

---

## 📡 API Endpoints

All endpoints are read-only (GET only). Base URL: `/api/raw/`

### 1. Products API
```
GET /api/raw/products/                    # List all products
GET /api/raw/products/{id}/               # Get specific product
```

**Response Example:**
```json
{
  "count": 150,
  "next": "http://localhost:8000/api/raw/products/?page=2",
  "previous": null,
  "results": [
    {
      "product_id": 1,
      "product_name": "Ankara Dress",
      "description": "Beautiful traditional dress",
      "artisan_id": 2,
      "category_id": 3,
      "price": "85.50",
      "currency_code": "USD",
      "sku": "DRESS-001",
      "stock_quantity": 15,
      "reorder_level": 10,
      "is_featured": true,
      "is_active": true,
      "average_rating": "4.75",
      "review_count": 12,
      "total_sales": 45,
      "created_at": "2026-04-20T10:30:00Z",
      "updated_at": "2026-04-25T14:15:00Z"
    }
  ]
}
```

### 2. Categories API
```
GET /api/raw/categories/                  # List all categories
GET /api/raw/categories/{id}/             # Get specific category
```

**Response Example:**
```json
{
  "count": 6,
  "results": [
    {
      "category_id": 1,
      "category_name": "Textiles",
      "description": "Traditional fabrics and textiles",
      "parent_category_id": null,
      "is_active": true,
      "display_order": 1,
      "created_at": "2026-04-20T10:00:00Z",
      "updated_at": "2026-04-20T10:00:00Z"
    }
  ]
}
```

### 3. Users API
```
GET /api/raw/users/                       # List all users
GET /api/raw/users/{id}/                  # Get specific user
```

**Response Example:**
```json
{
  "count": 10,
  "results": [
    {
      "user_id": 1,
      "username": "artisan1",
      "email": "artisan1@example.com",
      "password_hash": "$2b$12$...",
      "first_name": "Marie",
      "last_name": "Angelle",
      "phone_number": "+1234567890",
      "is_artisan": true,
      "is_admin": false,
      "is_active": true,
      "account_status": "active",
      "tier_id": 2,
      "email_verified": true,
      "email_verified_at": "2026-04-20T10:00:00Z",
      "last_login": "2026-04-25T09:00:00Z",
      "created_at": "2026-04-20T10:00:00Z",
      "updated_at": "2026-04-25T09:00:00Z"
    }
  ]
}
```

### 4. Orders API
```
GET /api/raw/orders/                      # List all orders
GET /api/raw/orders/{id}/                 # Get specific order
```

**Response Example:**
```json
{
  "count": 25,
  "results": [
    {
      "order_id": 1,
      "customer_id": 4,
      "order_number": "ORD-2026-001",
      "order_date": "2026-04-22T15:30:00Z",
      "status": "delivered",
      "currency_code": "USD",
      "subtotal": "170.00",
      "tax_amount": "12.75",
      "shipping_cost": "10.00",
      "discount_amount": "5.00",
      "total_amount": "187.75",
      "payment_method": "credit_card",
      "payment_status": "completed",
      "shipping_address": "123 Main St, New York, NY 10001",
      "billing_address": "123 Main St, New York, NY 10001",
      "notes": "Please handle with care",
      "created_at": "2026-04-22T15:30:00Z",
      "updated_at": "2026-04-25T10:00:00Z",
      "shipped_at": "2026-04-23T08:00:00Z",
      "delivered_at": "2026-04-25T14:30:00Z"
    }
  ]
}
```

### 5. Order Items API
```
GET /api/raw/order-items/                 # List all order items
GET /api/raw/order-items/{id}/            # Get specific order item
```

**Response Example:**
```json
{
  "count": 50,
  "results": [
    {
      "order_item_id": 1,
      "order_id": 1,
      "product_id": 2,
      "artisan_id": 3,
      "quantity": 2,
      "unit_price": "85.50",
      "subtotal": "171.00",
      "created_at": "2026-04-22T15:30:00Z"
    }
  ]
}
```

### 6. Cart Items API
```
GET /api/raw/cart-items/                  # List all cart items
GET /api/raw/cart-items/{id}/             # Get specific cart item
```

**Response Example:**
```json
{
  "count": 30,
  "results": [
    {
      "cart_item_id": 1,
      "cart_id": 2,
      "product_id": 5,
      "quantity": 3,
      "unit_price": "45.00",
      "subtotal": "135.00",
      "added_at": "2026-04-25T12:00:00Z"
    }
  ]
}
```

### 7. Additional Endpoints

```
GET /api/raw/customer-tiers/               # List all customer tiers
GET /api/raw/carts/                        # List all shopping carts
GET /api/raw/currencies/                   # List all supported currencies
```

---

## 🔍 Query Features

### Pagination

All endpoints support pagination with 20 items per page by default.

```
GET /api/raw/products/                    # Page 1 (default)
GET /api/raw/products/?page=2              # Page 2
GET /api/raw/products/?page_size=50        # 50 items per page (max 100)
```

### Search

Search across multiple fields:

```
GET /api/raw/products/?search=Ankara       # Search product names
GET /api/raw/users/?search=marie           # Search user names/emails
GET /api/raw/categories/?search=textile    # Search category names
GET /api/raw/orders/?search=ORD-2026       # Search order numbers
```

### Ordering

Sort by any field in ascending or descending order:

```
GET /api/raw/products/?ordering=-created_at    # Newest first
GET /api/raw/products/?ordering=price          # Cheapest first
GET /api/raw/products/?ordering=-average_rating # Highest rated first
GET /api/raw/orders/?ordering=-order_date      # Most recent orders

# Available ordering fields per endpoint:
# products: product_id, product_name, price, stock_quantity, average_rating, created_at
# users: user_id, username, email, is_artisan, is_admin, created_at
# orders: order_id, order_number, order_date, status, total_amount, payment_status
# categories: category_id, category_name, is_active, display_order
```

### Combined Filters

```
GET /api/raw/products/?page=2&page_size=50&search=Dress&ordering=-price
GET /api/raw/orders/?ordering=-order_date&page=1
GET /api/raw/users/?search=artisan&page_size=10
```

---

## 💾 Database Schema Exposed

### Tables Directly Accessible via API

| Table | Endpoint | Fields Exposed |
|-------|----------|-----------------|
| users | `/api/raw/users/` | All user fields (id, username, email, etc.) |
| products | `/api/raw/products/` | All product fields |
| categories | `/api/raw/categories/` | All category fields |
| orders | `/api/raw/orders/` | All order fields |
| order_items | `/api/raw/order-items/` | All order item fields |
| cart_items | `/api/raw/cart-items/` | All cart item fields |
| carts | `/api/raw/carts/` | All cart fields |
| customer_tiers | `/api/raw/customer-tiers/` | All tier fields |
| currencies | `/api/raw/currencies/` | All currency fields |

### Model Configuration

All models use `managed=False`:
```python
class Meta:
    managed = False
    db_table = 'actual_table_name'
```

This ensures Django:
- ✅ Does NOT create migrations
- ✅ Does NOT modify the database schema
- ✅ Only reads from existing tables
- ✅ Maps Python models to existing SQL tables

---

## 🔐 Security & Access

### Read-Only Access
- ✅ GET requests allowed
- ❌ POST requests blocked
- ❌ PUT requests blocked
- ❌ DELETE requests blocked
- ❌ No data modification possible

### Response Format
- All responses in JSON
- Consistent structure with `count`, `next`, `previous`, `results`
- Proper HTTP status codes (200, 404, 400)

---

## 📊 Example Queries for Academic Study

### Query 1: Find all active products with ratings
```
GET /api/raw/products/?search=&ordering=-average_rating&page_size=100
```

Use this to:
- Understand how ratings are stored
- See product structure
- Analyze pricing and inventory

### Query 2: Get artisan details
```
GET /api/raw/users/?search=artisan&page_size=50
```

Use this to:
- See all artisan profiles
- Understand user table structure
- Verify artisan flags

### Query 3: Analyze order structure
```
GET /api/raw/orders/?ordering=-order_date&page_size=20
GET /api/raw/order-items/?page_size=100
```

Use this to:
- Understand order relationships
- See how order_items link to orders and products
- Analyze payment status and order status

### Query 4: Inventory analysis
```
GET /api/raw/products/?ordering=-stock_quantity
```

Use this to:
- See inventory levels
- Identify stock quantity tracking
- Understand reorder levels

---

## 🎓 Learning Objectives

This API demonstrates:

1. **Database-First Architecture**
   - Models created after database exists
   - `managed=False` configuration
   - No migrations required

2. **SQL to REST Mapping**
   - Direct table-to-endpoint mapping
   - Flat JSON vs nested relationships
   - Foreign key representation

3. **REST API Best Practices**
   - Read-only operations for data integrity
   - Pagination for large datasets
   - Search and filtering capabilities
   - Proper HTTP methods and status codes

4. **Django ORM with External Databases**
   - Using existing tables
   - No Django schema management
   - Foreign key handling

5. **API Design Patterns**
   - Consistent response format
   - Proper URL structure
   - Query parameter conventions

---

## 🚀 Running the API

### Prerequisites
- Python 3.8+
- Django 6.0+
- Django REST Framework
- PostgreSQL (Neon) database

### Setup

1. **Activate Virtual Environment**
```bash
cd ecommerce/afribazaar
source .venv/Scripts/activate  # Windows
# or
source .venv/bin/activate       # Mac/Linux
```

2. **Install Dependencies**
```bash
pip install djangorestframework
```

3. **Run Development Server**
```bash
python manage.py runserver
```

4. **Access the API**
- API Root: `http://localhost:8000/api/raw/`
- Browsable API interface available at each endpoint
- JSON responses at all endpoints

### Testing Endpoints

**In Browser:**
```
http://localhost:8000/api/raw/products/
http://localhost:8000/api/raw/users/
http://localhost:8000/api/raw/orders/
```

**Using curl:**
```bash
curl http://localhost:8000/api/raw/products/
curl http://localhost:8000/api/raw/products/?page=2
curl http://localhost:8000/api/raw/products/?search=Dress
curl http://localhost:8000/api/raw/orders/?ordering=-order_date
```

**Using Python requests:**
```python
import requests

response = requests.get('http://localhost:8000/api/raw/products/')
products = response.json()
print(f"Total products: {products['count']}")
for product in products['results']:
    print(f"- {product['product_name']}: ${product['price']}")
```

---

## ✅ Validation Checklist for Professor

- [x] Database-first architecture implemented
- [x] Models use `managed=False` (NO migrations)
- [x] All fields exposed directly from database
- [x] Read-only access (GET only)
- [x] No business logic in API
- [x] Flat JSON responses (no nested serializers)
- [x] Pagination implemented
- [x] Search capabilities
- [x] Ordering capabilities
- [x] Separate from existing business API
- [x] Follows REST conventions
- [x] Consistent response format
- [x] Proper HTTP status codes
- [x] All 6 required tables exposed

---

## 📚 Related Documentation

- **SQL Schema**: See `afribazaar_database_schema.sql` for table definitions
- **Business API**: See `API_DOCUMENTATION.md` for complex API
- **Database Design**: See `SQL_SCHEMA_DOCUMENTATION.md` for educational content

---

## 🔧 Troubleshooting

### "No such table" error
- **Cause**: Database tables not created
- **Solution**: Run `afribazaar_database_schema.sql` in your PostgreSQL database

### "No migrations found"
- **Cause**: Django trying to run migrations
- **Solution**: This is expected! API_RAW doesn't use migrations - use `managed=False`

### Permission denied errors
- **Cause**: Trying to POST/PUT/DELETE
- **Solution**: API is read-only. These operations are intentionally blocked.

### Foreign key values instead of related objects
- **Expected behavior**: API returns FK ID values, not nested objects
- **This is correct** for database-first architecture

---

**API Version:** 1.0  
**Created:** April 25, 2026  
**Database:** PostgreSQL (Neon)  
**Purpose:** Academic Evaluation - Database-First REST API

