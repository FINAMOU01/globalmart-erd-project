# AfriBazaar E-Commerce Database Schema
## Complete SQL Design Documentation

---

## 📋 Document Overview

This document explains the complete database schema for the AfriBazaar e-commerce platform. The schema is designed as a production-ready relational database suitable for:
- E-commerce operations
- Advanced Database Systems coursework
- Educational demonstrations of database design principles
- Real-world application deployment

---

## 📊 Schema Statistics

| Metric | Count |
|--------|-------|
| **Total Tables** | 19 |
| **Relationships** | 28 (1:N and M:N) |
| **Constraints** | 45+ (PK, FK, UNIQUE, CHECK) |
| **Indexes** | 11 |
| **Views** | 4 |
| **Functions/Triggers** | 7 |
| **Seed Records** | 50+ |

---

## 🗄️ Table Structure Overview

### Core Tables (7)
1. **customer_tiers** - Loyalty/membership levels
2. **users** - All user accounts (customers, artisans, admins)
3. **categories** - Product categories
4. **products** - Product listings
5. **currencies** - Supported currencies
6. **exchange_rates** - Currency conversion rates
7. **warehouses** - Storage locations

### Product Management Tables (3)
8. **product_images** - Product photos
9. **product_attributes** - Attribute definitions (Color, Size, Material, etc.)
10. **product_attribute_values** - Predefined values for attributes
11. **inventory** - Stock tracking per warehouse

### Transaction Tables (6)
12. **carts** - Shopping cart per user
13. **cart_items** - Items in shopping carts
14. **orders** - Customer purchase orders
15. **order_items** - Products within orders
16. **artisan_ratings** - Customer reviews of artisans

---

## 🔑 Key Relationships

### One-to-Many Relationships (1:N)

```
users (1) ────→ (N) products
    │ Each user is an artisan with multiple products
    
users (1) ────→ (N) orders
    │ Each customer has multiple orders
    
users (1) ────→ (N) carts
    │ Each user has one active cart
    
customer_tiers (1) ────→ (N) users
    │ Each tier has many customers
    
categories (1) ────→ (N) products
    │ Each category has multiple products
    
products (1) ────→ (N) cart_items
    │ Each product can be in multiple carts
    
products (1) ────→ (N) order_items
    │ Each product can be in multiple orders
    
products (1) ────→ (N) product_images
    │ Each product has multiple images
    
orders (1) ────→ (N) order_items
    │ Each order has multiple items
    
inventory (1) ────→ (N) warehouses
    │ Each product has inventory in multiple warehouses
    
currencies (1) ────→ (N) exchange_rates
    │ Each currency has historical rates
```

### Many-to-Many Relationships (M:N)

```
products (M) ←──→ (N) product_attributes
    │ Implemented via: inventory and product characteristics
    │ A product can have multiple attributes
    │ An attribute can apply to multiple products
    
users (M) ←──→ (N) artisan_ratings
    │ Customers rate artisans
    │ Artisans can have multiple ratings
```

---

## 📐 Constraint Hierarchy

### PRIMARY KEY Constraints
Every table has a `*_id SERIAL PRIMARY KEY` as the unique identifier.

```sql
Example: product_id SERIAL PRIMARY KEY
```

### FOREIGN KEY Constraints
Foreign keys enforce referential integrity:

```sql
-- Products must reference existing artisans
artisan_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE RESTRICT

-- Order items must reference existing orders
order_id INTEGER NOT NULL REFERENCES orders(order_id) ON DELETE CASCADE
```

**DELETE Actions:**
- `ON DELETE RESTRICT` - Prevent deletion if referenced (e.g., artisans with products)
- `ON DELETE CASCADE` - Delete dependent records (e.g., order items when order is deleted)

### UNIQUE Constraints
Ensure uniqueness across specified columns:

```sql
-- Email must be unique per user
email VARCHAR(255) NOT NULL UNIQUE

-- Product SKU must be unique
sku VARCHAR(50) UNIQUE

-- One cart per user
user_id INTEGER NOT NULL UNIQUE REFERENCES users

-- Cart can have each product only once
UNIQUE(cart_id, product_id)
```

### CHECK Constraints
Enforce valid data values:

```sql
-- Email format validation (PostgreSQL regex)
CONSTRAINT valid_email CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$')

-- Positive prices
price NUMERIC(10, 2) NOT NULL CHECK (price > 0)

-- Valid rating (1-5)
rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5)

-- Status whitelist
status VARCHAR(20) CHECK (status IN ('pending', 'confirmed', 'processing', 'shipped', 'delivered'))

-- Percentage bounds
discount_percentage NUMERIC(5, 2) CHECK (discount_percentage >= 0 AND discount_percentage <= 100)

-- Inventory constraint (available = on_hand - reserved)
CHECK (quantity_available = quantity_on_hand - quantity_reserved)
```

### DEFAULT Values
Auto-populated fields:

```sql
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
is_active BOOLEAN DEFAULT TRUE
tier_id INTEGER NOT NULL DEFAULT 1
```

---

## 🔍 Table Specifications

### 1. customer_tiers
**Purpose:** Define loyalty program levels with discount tiers

| Column | Type | Constraints | Purpose |
|--------|------|-------------|---------|
| tier_id | SERIAL | PK | Unique tier identifier |
| tier_name | VARCHAR(50) | UNIQUE, NOT NULL | Tier name (Bronze, Silver, Gold, Platinum) |
| min_annual_spend | NUMERIC | CHECK ≥ 0 | Minimum spending to achieve tier |
| discount_percentage | NUMERIC | CHECK 0-100 | Discount percentage for tier |
| benefits_description | TEXT | | Human-readable benefits |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |

**Seed Data:**
- Bronze: $0 spend, 0% discount
- Silver: $500 spend, 5% discount
- Gold: $2000 spend, 10% discount
- Platinum: $5000 spend, 15% discount

---

### 2. users
**Purpose:** Store all user accounts (customers, artisans, admins)

| Column | Type | Key Constraints | Purpose |
|--------|------|-----------------|---------|
| user_id | SERIAL | PK | Unique user identifier |
| username | VARCHAR(50) | UNIQUE, NOT NULL | Login username |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User email with regex validation |
| password_hash | VARCHAR(255) | NOT NULL | Bcrypt hashed password |
| first_name | VARCHAR(100) | | User's first name |
| is_artisan | BOOLEAN | DEFAULT FALSE | Flag: is this user an artisan? |
| is_admin | BOOLEAN | DEFAULT FALSE | Flag: is this user an admin? |
| tier_id | INTEGER | FK → customer_tiers | Customer loyalty tier |
| account_status | VARCHAR(20) | CHECK status | Status: active, suspended, deleted, pending_verification |
| created_at | TIMESTAMP | DEFAULT NOW() | Account creation time |

**Relationships:**
- Foreign Key: tier_id → customer_tiers.tier_id (NOT NULL DEFAULT 1)

**Indexes:**
- email (for fast login lookups)
- tier_id (for tier analysis)
- is_artisan (for artisan listings)

---

### 3. categories
**Purpose:** Organize products into hierarchical categories

| Column | Type | Constraints | Purpose |
|--------|------|-------------|---------|
| category_id | SERIAL | PK | Unique category identifier |
| category_name | VARCHAR(100) | UNIQUE, NOT NULL | Category name |
| description | TEXT | | Category description |
| parent_category_id | INTEGER | FK (self-referential) | Parent category for hierarchy |
| is_active | BOOLEAN | DEFAULT TRUE | Is category visible? |
| display_order | INTEGER | DEFAULT 0 | Sort order in UI |

**Relationships:**
- Self-referential FK: parent_category_id → categories.category_id

**Hierarchical Structure:**
```
Fashion & Clothing
├── Men's Clothing
└── Women's Clothing

Home & Decor
├── Wall Art
└── Sculptures
```

---

### 4. currencies
**Purpose:** Define supported currencies for international transactions

| Column | Type | Constraints | Purpose |
|--------|------|-------------|---------|
| currency_code | CHAR(3) | PK | ISO 4217 code (USD, EUR, NGN, etc.) |
| currency_name | VARCHAR(50) | NOT NULL | Full name (US Dollar, Nigerian Naira) |
| currency_symbol | VARCHAR(5) | NOT NULL | Display symbol ($, €, ₦) |
| is_active | BOOLEAN | DEFAULT TRUE | Is currency in use? |
| decimal_places | INTEGER | CHECK 0-8 | Number of decimal places |

**Seed Data (10 currencies):**
- USD, EUR, GBP (Western currencies)
- XAF, NGN, GHS, KES, ZAR, EGP, MAD (African currencies)

---

### 5. exchange_rates
**Purpose:** Track historical exchange rates for currency conversion

**Exchange Rate Logic:**
```
Price in USD = Price in Currency × rate_to_usd

Example:
- 1 XAF (CFA Franc) = 0.00165 USD
- 100 XAF = 0.165 USD

- 1 EUR = 1.08 USD
- 100 EUR = 108 USD
```

| Column | Type | Constraints | Purpose |
|--------|------|-------------|---------|
| exchange_rate_id | SERIAL | PK | Unique rate identifier |
| currency_code | CHAR(3) | FK → currencies | Currency code |
| rate_to_usd | NUMERIC(18,8) | CHECK > 0 | Exchange rate to USD |
| effective_date | DATE | | Date rate became effective |
| created_at | TIMESTAMP | DEFAULT NOW() | When rate was recorded |

**Unique Constraint:** (currency_code, effective_date)
- Prevents duplicate rates for same currency on same day

---

### 6. product_attributes
**Purpose:** Define reusable product attributes (Color, Size, Material, etc.)

| Column | Type | Constraints | Purpose |
|--------|------|-------------|---------|
| attribute_id | SERIAL | PK | Unique attribute identifier |
| attribute_name | VARCHAR(100) | UNIQUE | Attribute name |
| attribute_type | VARCHAR(50) | CHECK IN (...) | Type: text, number, select, multiselect |
| is_filterable | BOOLEAN | DEFAULT TRUE | Can be used as filter? |
| is_searchable | BOOLEAN | DEFAULT FALSE | Is searchable in full-text? |

**Types:**
- `text` - Free-form text (e.g., custom notes)
- `number` - Numeric value (e.g., measurements)
- `select` - Single choice from predefined values
- `multiselect` - Multiple choices

**Seed Data:**
- Color (select, filterable)
- Size (select, filterable)
- Material (text, searchable)
- Pattern (select)
- Gender (select, filterable)
- Occasion (multiselect, searchable)

---

### 7. product_attribute_values
**Purpose:** Define allowed values for select/multiselect attributes

| Column | Type | Constraints | Purpose |
|--------|------|-------------|---------|
| attribute_value_id | SERIAL | PK | Unique value identifier |
| attribute_id | INTEGER | FK → product_attributes | Parent attribute |
| value | VARCHAR(255) | NOT NULL | The actual value |
| display_order | INTEGER | DEFAULT 0 | Sort order |

**Unique Constraint:** (attribute_id, value)
- Prevents duplicate values within an attribute

**Example (Color Attribute):**
```
attribute_id: 1 (Color)
├── Red
├── Blue
├── Yellow
├── Green
├── Black
├── White
└── Multicolor
```

---

### 8. products
**Purpose:** Core product information

| Column | Type | Constraints | Purpose |
|--------|------|-------------|---------|
| product_id | SERIAL | PK | Unique product identifier |
| product_name | VARCHAR(255) | NOT NULL | Product title |
| description | TEXT | | Detailed description |
| artisan_id | INTEGER | FK → users (NOT NULL) | Creator/seller |
| category_id | INTEGER | FK → categories (NOT NULL) | Product category |
| price | NUMERIC(10,2) | CHECK > 0 | Product price |
| currency_code | CHAR(3) | FK → currencies (DEFAULT 'USD') | Price currency |
| sku | VARCHAR(50) | UNIQUE | Stock Keeping Unit |
| stock_quantity | INTEGER | CHECK ≥ 0 | Total stock (sum of warehouses) |
| reorder_level | INTEGER | CHECK ≥ 0 | When to reorder |
| is_featured | BOOLEAN | DEFAULT FALSE | Featured on homepage? |
| is_active | BOOLEAN | DEFAULT TRUE | Is product for sale? |
| average_rating | NUMERIC(3,2) | CHECK 0-5 | Average customer rating |
| review_count | INTEGER | CHECK ≥ 0 | Total reviews |
| total_sales | INTEGER | CHECK ≥ 0 | Lifetime units sold |

**Relationships:**
- artisan_id: NOT NULL (requires artisan)
- category_id: NOT NULL (requires category)

**Indexes:**
- artisan_id (find all products by artisan)
- category_id (find products in category)
- is_active (filter active products)

**Denormalized Fields:**
- stock_quantity: Updated by trigger from inventory table
- average_rating: Updated by triggers from ratings

---

### 9. product_images
**Purpose:** Store multiple images per product

| Column | Type | Constraints | Purpose |
|--------|------|-------------|---------|
| image_id | SERIAL | PK | Unique image identifier |
| product_id | INTEGER | FK → products (CASCADE) | Parent product |
| image_url | VARCHAR(500) | NOT NULL | Image URL/path |
| alt_text | VARCHAR(255) | | Accessibility alt text |
| is_primary | BOOLEAN | DEFAULT FALSE | Is this the main image? |
| display_order | INTEGER | DEFAULT 0 | Sort order in gallery |

**Unique Constraint:** (product_id, image_url)
- Prevents duplicate images for same product

---

### 10. warehouses
**Purpose:** Define physical/logical inventory storage locations

| Column | Type | Constraints | Purpose |
|--------|------|-------------|---------|
| warehouse_id | SERIAL | PK | Unique warehouse identifier |
| warehouse_name | VARCHAR(100) | UNIQUE | Warehouse name |
| warehouse_code | VARCHAR(20) | UNIQUE | Short code (WH-001, WH-002) |
| address | TEXT | NOT NULL | Physical address |
| city | VARCHAR(50) | | City location |
| country | VARCHAR(50) | | Country |
| capacity | INTEGER | CHECK > 0 | Total storage capacity |
| is_active | BOOLEAN | DEFAULT TRUE | Is warehouse operational? |

**Seed Data:**
- Lagos, Nigeria (Main Warehouse)
- Accra, Ghana (Distribution Center)
- Dakar, Senegal (Fulfillment Hub)
- Cairo, Egypt (Regional Hub)

---

### 11. inventory
**Purpose:** Track product quantities per warehouse

**Inventory Logic:**
```
quantity_available = quantity_on_hand - quantity_reserved

Scenario:
- Product has 100 units on hand
- 30 units reserved for pending orders
- Available for purchase: 70 units
```

| Column | Type | Constraints | Purpose |
|--------|------|-------------|---------|
| inventory_id | SERIAL | PK | Unique inventory record |
| product_id | INTEGER | FK → products (CASCADE) | Product |
| warehouse_id | INTEGER | FK → warehouses | Warehouse location |
| quantity_on_hand | INTEGER | CHECK ≥ 0 | Physical stock |
| quantity_reserved | INTEGER | CHECK ≥ 0 | Reserved for orders |
| quantity_available | INTEGER | CHECK ≥ 0 | Available to purchase |
| reorder_point | INTEGER | CHECK ≥ 0 | Auto-reorder threshold |
| last_restocked_at | TIMESTAMP | | Last restock date |

**Unique Constraint:** (product_id, warehouse_id)
- One inventory record per product per warehouse

**CHECK Constraint:**
```sql
CHECK (quantity_available = quantity_on_hand - quantity_reserved)
```
- Enforced and maintained by trigger

**Trigger:** `trg_update_inventory_available`
- Automatically calculates `quantity_available` before insert/update
- Prevents inventory inconsistencies

---

### 12. carts
**Purpose:** Shopping cart for each user (one active cart per user)

| Column | Type | Constraints | Purpose |
|--------|------|-------------|---------|
| cart_id | SERIAL | PK | Unique cart identifier |
| user_id | INTEGER | UNIQUE FK → users | User who owns cart |
| total_items | INTEGER | CHECK ≥ 0 | Total items in cart |
| subtotal | NUMERIC(12,2) | CHECK ≥ 0 | Sum of all item prices |
| created_at | TIMESTAMP | DEFAULT NOW() | Cart creation time |
| updated_at | TIMESTAMP | DEFAULT NOW() | Last update time |
| expires_at | TIMESTAMP | DEFAULT NOW() + 30 days | Expiration for abandoned carts |

**Unique Constraint:** user_id UNIQUE
- Each user has exactly one active cart

**Trigger:** `trg_update_cart_totals`
- Automatically recalculates `total_items` and `subtotal` when items added/removed

---

### 13. cart_items
**Purpose:** Individual items in a shopping cart

| Column | Type | Constraints | Purpose |
|--------|------|-------------|---------|
| cart_item_id | SERIAL | PK | Unique cart item |
| cart_id | INTEGER | FK → carts (CASCADE) | Parent cart |
| product_id | INTEGER | FK → products | Product in cart |
| quantity | INTEGER | CHECK > 0 | Quantity (min 1) |
| unit_price | NUMERIC(10,2) | CHECK > 0 | Price at time added |
| subtotal | NUMERIC(12,2) | GENERATED | quantity × unit_price |

**Unique Constraint:** (cart_id, product_id)
- Each product appears only once in cart (quantity field for multiples)

**Generated Column:**
```sql
subtotal NUMERIC(12,2) GENERATED ALWAYS AS (quantity * unit_price) STORED
```
- Automatically calculated and stored
- Prevents manual errors

---

### 14. orders
**Purpose:** Customer purchase orders

**Order Status Workflow:**
```
pending → confirmed → processing → shipped → delivered
                   ↓
                cancelled
                   ↓
                returned
```

| Column | Type | Constraints | Purpose |
|--------|------|-------------|---------|
| order_id | SERIAL | PK | Unique order identifier |
| customer_id | INTEGER | FK → users (RESTRICT) | Customer who placed order |
| order_number | VARCHAR(50) | UNIQUE | Human-readable order ID (ORD-2026-001) |
| order_date | TIMESTAMP | DEFAULT NOW() | When order was placed |
| status | VARCHAR(30) | CHECK status | Order status |
| currency_code | CHAR(3) | FK → currencies | Currency for pricing |
| subtotal | NUMERIC(12,2) | CHECK ≥ 0 | Items total |
| tax_amount | NUMERIC(12,2) | CHECK ≥ 0 | Tax calculated |
| shipping_cost | NUMERIC(12,2) | CHECK ≥ 0 | Shipping fee |
| discount_amount | NUMERIC(12,2) | CHECK ≥ 0 | Applied discount |
| total_amount | NUMERIC(12,2) | CHECK ≥ 0 | Final total |
| payment_method | VARCHAR(50) | | credit_card, paypal, bank_transfer, etc. |
| payment_status | VARCHAR(20) | CHECK status | pending, processing, completed, failed, refunded |
| shipping_address | TEXT | | Delivery address |
| billing_address | TEXT | | Billing address |
| notes | TEXT | | Order notes |
| created_at | TIMESTAMP | DEFAULT NOW() | Order creation |
| updated_at | TIMESTAMP | DEFAULT NOW() | Last update |
| shipped_at | TIMESTAMP | | When shipped |
| delivered_at | TIMESTAMP | | When delivered |

**Status Values:**
- `pending` - Order received, awaiting confirmation
- `confirmed` - Customer confirmed payment
- `processing` - Being prepared for shipment
- `shipped` - In transit
- `delivered` - Successfully delivered
- `cancelled` - Customer cancelled
- `returned` - Product returned by customer

**Payment Status:**
- `pending` - Awaiting payment
- `processing` - Payment processing
- `completed` - Payment successful
- `failed` - Payment failed
- `refunded` - Order refunded

**Indexes:**
- customer_id (find customer's orders)
- order_date (sort by date)
- status (filter by status)

---

### 15. order_items
**Purpose:** Individual products within an order

| Column | Type | Constraints | Purpose |
|--------|------|-------------|---------|
| order_item_id | SERIAL | PK | Unique order item |
| order_id | INTEGER | FK → orders (CASCADE) | Parent order |
| product_id | INTEGER | FK → products | Product ordered |
| artisan_id | INTEGER | FK → users | Artisan/seller |
| quantity | INTEGER | CHECK > 0 | Quantity ordered |
| unit_price | NUMERIC(10,2) | CHECK > 0 | Price at order time |
| subtotal | NUMERIC(12,2) | GENERATED | quantity × unit_price |
| created_at | TIMESTAMP | DEFAULT NOW() | Item added to order |

**Generated Column:**
```sql
subtotal NUMERIC(12,2) GENERATED ALWAYS AS (quantity * unit_price) STORED
```

**Purpose of Denormalization:**
- artisan_id stored with item (no need to join products)
- unit_price stored (product price may change later)
- Ensures historical accuracy of orders

---

### 16. artisan_ratings
**Purpose:** Customer reviews and ratings for artisans

| Column | Type | Constraints | Purpose |
|--------|------|-------------|---------|
| rating_id | SERIAL | PK | Unique rating |
| artisan_id | INTEGER | FK → users (CASCADE) | Rated artisan |
| customer_id | INTEGER | FK → users (CASCADE) | Rating customer |
| rating | INTEGER | CHECK 1-5 | Star rating (1-5) |
| review_title | VARCHAR(200) | | Review headline |
| review_text | TEXT | | Detailed review |
| is_verified_purchase | BOOLEAN | DEFAULT FALSE | Purchased from artisan? |
| helpful_count | INTEGER | CHECK ≥ 0 | People found helpful |
| created_at | TIMESTAMP | DEFAULT NOW() | When reviewed |
| updated_at | TIMESTAMP | DEFAULT NOW() | Last modified |

**Unique Constraint:** (artisan_id, customer_id)
- Each customer rates each artisan only once

**Rating Scale:**
- 1: ⭐ Poor
- 2: ⭐⭐ Fair
- 3: ⭐⭐⭐ Good
- 4: ⭐⭐⭐⭐ Very Good
- 5: ⭐⭐⭐⭐⭐ Excellent

---

## 📈 Views (Analytical Queries)

### View 1: v_active_products_summary
**Purpose:** Quick view of active products with related data

**Query Result:**
```sql
SELECT
    product_id, product_name, artisan_name, category_name,
    price, currency_code, stock_quantity, average_rating, review_count
FROM v_active_products_summary
WHERE is_featured = TRUE
ORDER BY average_rating DESC;
```

### View 2: v_customer_order_history
**Purpose:** Customer order summaries

**Query Result:**
```sql
SELECT * FROM v_customer_order_history
WHERE customer_name = 'Marie Angelle'
ORDER BY order_date DESC;
```

### View 3: v_inventory_status
**Purpose:** Real-time inventory across warehouses

**Stock Status Indicators:**
- `Out of Stock` - quantity_available = 0
- `Low Stock` - quantity_available ≤ reorder_point
- `In Stock` - quantity_available > reorder_point

### View 4: v_artisan_performance
**Purpose:** Artisan sales and ratings analytics

**Metrics Shown:**
- Total products listed
- Total items sold
- Review count
- Average rating (rounded to 2 decimals)

### View 5: v_customer_tier_analysis
**Purpose:** Customer spending analysis and tier eligibility

**Calculations:**
- Annual spending (last 12 months)
- Order count (last 12 months)
- Current tier and discount percentage

---

## 🔧 Functions & Triggers

### Function 1: fn_calculate_order_total()
**Purpose:** Calculate final order total from components

**Formula:**
```
total = subtotal + tax + shipping - discount
```

### Function 2: fn_update_inventory_available()
**Trigger:** BEFORE INSERT OR UPDATE on inventory
**Purpose:** Maintain inventory_available = on_hand - reserved

**Action:** Raises exception if calculation results in negative available

### Function 3: fn_update_product_stock()
**Trigger:** AFTER INSERT/UPDATE/DELETE on inventory
**Purpose:** Denormalize total stock from all warehouses into products table

**Benefit:** Fast product queries without joining inventory

### Function 4: fn_update_cart_totals()
**Trigger:** AFTER INSERT/UPDATE/DELETE on cart_items
**Purpose:** Automatically recalculate cart totals

**Updates:**
- total_items = SUM(quantity)
- subtotal = SUM(subtotal)

### Function 5: fn_update_timestamp()
**Trigger:** BEFORE UPDATE on products, orders, users, etc.
**Purpose:** Keep updated_at timestamps current

---

## 🎓 Educational Use Cases

### Database Design Principles Demonstrated

1. **Normalization (Up to 3NF)**
   - Eliminates data redundancy
   - Improves data integrity
   - Example: Exchange rates stored separately from currencies

2. **Referential Integrity**
   - Foreign keys prevent orphaned records
   - CASCADE delete removes dependent data
   - RESTRICT prevents deletion of referenced data

3. **Constraints & Validation**
   - Email regex validation
   - Price positivity checks
   - Status whitelisting
   - Range checking (ratings 1-5)

4. **Denormalization for Performance**
   - Average rating stored on products
   - Stock quantity aggregated on products
   - Enables faster queries at cost of update triggers

5. **Triggers & Automation**
   - Automatic timestamp updates
   - Inventory calculations
   - Cart total recalculation
   - Real-time data synchronization

6. **Indexes for Query Optimization**
   - B-tree indexes on foreign keys
   - Separate index for search fields
   - Improves query performance 100-1000x

7. **Views for Data Abstraction**
   - Hide complexity from users
   - Pre-calculated aggregations
   - Consistent business logic

8. **Seed Data for Testing**
   - Realistic data for demonstrations
   - Relationships and constraints exercised
   - Ready for educational scenarios

---

## 📊 Sample Queries for Learning

### Query 1: Find top artisans by sales volume
```sql
SELECT 
    a.artisan_name, 
    SUM(oi.quantity) as total_sold,
    COUNT(DISTINCT o.order_id) as order_count,
    a.average_rating
FROM v_artisan_performance a
ORDER BY total_sold DESC
LIMIT 10;
```

### Query 2: Calculate customer lifetime value with tier upgrade eligibility
```sql
SELECT 
    c.customer_name,
    c.annual_spend,
    c.tier_name,
    CASE 
        WHEN c.annual_spend >= 5000 THEN 'Platinum'
        WHEN c.annual_spend >= 2000 THEN 'Gold'
        WHEN c.annual_spend >= 500 THEN 'Silver'
        ELSE 'Bronze'
    END as eligible_tier,
    (SELECT tier_id FROM customer_tiers 
     WHERE tier_name = 
        CASE 
            WHEN c.annual_spend >= 5000 THEN 'Platinum'
            WHEN c.annual_spend >= 2000 THEN 'Gold'
            WHEN c.annual_spend >= 500 THEN 'Silver'
            ELSE 'Bronze'
        END) as new_tier_id
FROM v_customer_tier_analysis c
WHERE c.annual_spend > 0;
```

### Query 3: Find inventory issues
```sql
SELECT * FROM v_inventory_status
WHERE stock_status != 'In Stock'
ORDER BY warehouse_name, product_name;
```

### Query 4: Calculate USD-equivalent prices
```sql
SELECT 
    p.product_name,
    p.price,
    p.currency_code,
    (p.price * er.rate_to_usd) as price_in_usd
FROM products p
JOIN exchange_rates er ON p.currency_code = er.currency_code
WHERE er.effective_date = CURRENT_DATE
ORDER BY price_in_usd DESC;
```

### Query 5: Find abandoned carts
```sql
SELECT 
    c.cart_id,
    u.email,
    COUNT(ci.cart_item_id) as item_count,
    c.subtotal,
    c.updated_at
FROM carts c
JOIN users u ON c.user_id = u.user_id
LEFT JOIN cart_items ci ON c.cart_id = ci.cart_id
WHERE c.expires_at < CURRENT_TIMESTAMP
GROUP BY c.cart_id, u.email, c.subtotal, c.updated_at;
```

---

## ✅ Production Readiness Checklist

- [x] All primary keys defined
- [x] All foreign keys with DELETE actions specified
- [x] UNIQUE constraints where needed
- [x] CHECK constraints for data validation
- [x] Email regex validation
- [x] Positive value constraints
- [x] Timestamp tracking (created_at, updated_at)
- [x] Indexes on frequently queried columns
- [x] Views for common analytical queries
- [x] Triggers for data consistency
- [x] Seed data for testing
- [x] PostgreSQL compatibility
- [x] Proper naming conventions
- [x] Clear documentation
- [x] Hierarchical categories support
- [x] Multi-warehouse inventory
- [x] Multi-currency support
- [x] Historical exchange rates
- [x] Audit trail (timestamps)
- [x] Soft deletes support (is_active flag)

---

## 🚀 How to Use This Schema

### 1. **Run the SQL Script**
```sql
-- Connect to your PostgreSQL/Neon database
\c afribazaar

-- Execute the entire schema script
\i afribazaar_database_schema.sql

-- Verify tables created
SELECT * FROM information_schema.tables 
WHERE table_schema = 'public';
```

### 2. **Add More Data**
```sql
-- Insert more customers
INSERT INTO users (...) VALUES (...);

-- Insert more products
INSERT INTO products (...) VALUES (...);

-- Create orders
INSERT INTO orders (...) VALUES (...);
INSERT INTO order_items (...) VALUES (...);
```

### 3. **Write Analytical Queries**
```sql
-- Use the views for analysis
SELECT * FROM v_customer_tier_analysis;
SELECT * FROM v_artisan_performance;
SELECT * FROM v_inventory_status;
```

### 4. **Maintain Data Quality**
```sql
-- Check for inventory inconsistencies
SELECT * FROM inventory 
WHERE quantity_available != (quantity_on_hand - quantity_reserved);

-- Find products with missing categories
SELECT * FROM products WHERE category_id IS NULL;

-- Verify exchange rates are current
SELECT * FROM exchange_rates WHERE effective_date < CURRENT_DATE - INTERVAL '1 month';
```

---

## 📚 Learning Resources

### Topics Covered
- **Relational Database Design**
- **Normalization (1NF, 2NF, 3NF)**
- **Entity-Relationship Modeling**
- **Referential Integrity**
- **Constraints & Validation**
- **Indexing Strategies**
- **Query Optimization**
- **Stored Procedures & Triggers**
- **Views & Abstraction**
- **Multi-currency Systems**
- **Inventory Management**
- **E-commerce Systems**

### Extensions for Advanced Topics
1. **Partitioning** - Partition orders by year
2. **Replication** - Set up read replicas
3. **Backup/Recovery** - Implement PITR (Point-In-Time Recovery)
4. **Performance Tuning** - Analyze query plans
5. **Security** - Row-level security (RLS)
6. **Temporal Tables** - Track historical changes
7. **Full-Text Search** - Search product descriptions
8. **JSON Support** - Store flexible product attributes

---

## 📋 Summary

This database schema provides:
- ✅ Production-ready structure for e-commerce platform
- ✅ Comprehensive constraint system for data integrity
- ✅ Realistic seed data for testing
- ✅ Educational examples of database design principles
- ✅ PostgreSQL/Neon compatibility
- ✅ Performance optimization through indexing
- ✅ Data consistency through triggers
- ✅ Analytical views for business intelligence
- ✅ Well-documented for learning purposes

The schema can be used for:
- Running an actual AfriBazaar e-commerce platform
- Learning database design principles
- Teaching Advanced Database Systems course
- Interview preparation
- Portfolio demonstration

---

**Schema Version:** 1.0  
**Created:** April 25, 2026  
**Database:** PostgreSQL 12+ (Neon compatible)  
**License:** Educational Use

