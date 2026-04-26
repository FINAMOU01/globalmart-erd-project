# AfriBazaar REST API Documentation

## Overview

The AfriBazaar REST API exposes the existing PostgreSQL database through read-only endpoints. All responses are in JSON format. The API uses pagination, filtering, and search capabilities to make data easy to consume.

**Base URL:** `http://localhost:8000/api/` (development)

**Format:** JSON

**Authentication:** Not required for now (public read access)

---

## API Features

✅ **Pagination** — Get large datasets in manageable chunks (20 items per page by default)
✅ **Filtering** — Filter orders by status, products by category/artisan
✅ **Search** — Full-text search across multiple fields
✅ **Ordering** — Sort results by various fields (ascending/descending)
✅ **Nested Data** — Related objects included in responses (e.g., Product includes Category and Artisan)
✅ **Browsable API** — Visit endpoints in browser for interactive exploration
✅ **Lightweight Serializers** — List endpoints return condensed data for better performance

---

## Endpoints

### 1. PRODUCTS

#### List Products
```
GET /api/products/
```

**Query Parameters:**
- `page=1` — Page number (default: 1)
- `page_size=20` — Items per page (default: 20, max: 100)
- `search=ankara` — Search in name, description, artisan username
- `ordering=-created_at` — Sort by field (use `-` for descending)

**Response (Success):**
```json
{
  "count": 156,
  "next": "http://localhost:8000/api/products/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Authentic Ankara Fabric Dress",
      "artisan_name": "Amara Okafor",
      "category_name": "Textiles",
      "price": "45.99",
      "currency_code": "USD",
      "formatted_price": "45.99 USD",
      "stock_quantity": 12,
      "image": "http://localhost:8000/media/products/dress_001.jpg",
      "is_featured": true,
      "created_at": "2025-03-15T10:30:00Z"
    },
    {
      "id": 2,
      "name": "Hand-Carved Wooden Mask",
      "artisan_name": "Kofi Mensah",
      "category_name": "Masks",
      "price": "89.50",
      "currency_code": "USD",
      "formatted_price": "89.50 USD",
      "stock_quantity": 5,
      "image": "http://localhost:8000/media/products/mask_001.jpg",
      "is_featured": false,
      "created_at": "2025-03-14T14:20:00Z"
    }
  ]
}
```

#### Get Product Details
```
GET /api/products/{id}/
```

**Response (Success):**
```json
{
  "id": 1,
  "artisan": {
    "id": 5,
    "username": "amara_okafor",
    "email": "amara@example.com",
    "first_name": "Amara",
    "last_name": "Okafor",
    "is_artisan": true,
    "profile": {
      "id": 2,
      "phone": "+234-803-1234567",
      "address": "Lagos, Nigeria",
      "bio": "Traditional Ankara textiles and contemporary designs",
      "profile_picture": "http://localhost:8000/media/artisans/amara.jpg",
      "social_links": {
        "instagram": "@amara_textiles",
        "twitter": "@amara_art"
      },
      "is_verified": true,
      "currency_preference": "NGN",
      "date_joined": "2024-01-10T00:00:00Z",
      "average_rating": 4.8,
      "total_ratings": 24
    },
    "products_count": 18
  },
  "category": {
    "id": 3,
    "name": "Textiles",
    "description": "African textiles and fabrics",
    "image": "http://localhost:8000/media/categories/textiles.jpg",
    "created_at": "2024-01-01T00:00:00Z"
  },
  "name": "Authentic Ankara Fabric Dress",
  "description": "Beautiful hand-stitched dress made from premium Ankara fabric. Perfect for celebrations and everyday wear.",
  "price": "45.99",
  "currency_code": "USD",
  "formatted_price": "45.99 USD",
  "stock_quantity": 12,
  "image": "http://localhost:8000/media/products/dress_001.jpg",
  "attributes": {
    "color": "Royal Blue",
    "size": "M",
    "material": "100% Cotton Ankara",
    "care": "Hand wash recommended"
  },
  "is_featured": true,
  "created_at": "2025-03-15T10:30:00Z",
  "updated_at": "2025-03-20T08:15:00Z"
}
```

#### Featured Products
```
GET /api/products/featured/
```

Returns only products with `is_featured=true`. Same pagination and filtering as list endpoint.

#### Products by Category
```
GET /api/products/by_category/?category_id=3
```

**Required Parameters:**
- `category_id` — ID of the category

#### Products by Artisan
```
GET /api/products/by_artisan/?artisan_id=5
```

**Required Parameters:**
- `artisan_id` — ID of the artisan (User ID)

---

### 2. ARTISANS

#### List Artisans
```
GET /api/artisans/
```

**Query Parameters:**
- `search=kofi` — Search in username, first_name, last_name, email
- `ordering=username` — Sort by field
- `page_size=20` — Items per page

**Response (Success):**
```json
{
  "count": 45,
  "next": "http://localhost:8000/api/artisans/?page=2",
  "previous": null,
  "results": [
    {
      "id": 5,
      "username": "amara_okafor",
      "email": "amara@example.com",
      "first_name": "Amara",
      "last_name": "Okafor",
      "is_artisan": true,
      "profile": {
        "id": 2,
        "phone": "+234-803-1234567",
        "address": "Lagos, Nigeria",
        "bio": "Traditional Ankara textiles and contemporary designs",
        "profile_picture": "http://localhost:8000/media/artisans/amara.jpg",
        "social_links": {
          "instagram": "@amara_textiles"
        },
        "is_verified": true,
        "currency_preference": "NGN",
        "date_joined": "2024-01-10T00:00:00Z",
        "average_rating": 4.8,
        "total_ratings": 24
      },
      "products_count": 18
    }
  ]
}
```

#### Get Artisan Details
```
GET /api/artisans/{id}/
```

Same structure as list response above.

#### Artisan's Products
```
GET /api/artisans/{id}/products/
```

Lists all products by this artisan (paginated).

#### Artisan's Ratings
```
GET /api/artisans/{id}/ratings/
```

Lists all reviews and ratings for this artisan.

---

### 3. CATEGORIES

#### List Categories
```
GET /api/categories/
```

**Query Parameters:**
- `search=textiles` — Search in name and description
- `ordering=name` — Sort by field

**Response (Success):**
```json
{
  "count": 12,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Beadwork",
      "description": "Intricate beaded jewelry and accessories",
      "image": "http://localhost:8000/media/categories/beadwork.jpg",
      "created_at": "2024-01-01T00:00:00Z"
    },
    {
      "id": 3,
      "name": "Textiles",
      "description": "African textiles and fabrics",
      "image": "http://localhost:8000/media/categories/textiles.jpg",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

#### Get Category Details
```
GET /api/categories/{id}/
```

Returns a single category object.

---

### 4. ORDERS

#### List Orders
```
GET /api/orders/
```

**Query Parameters:**
- `search=pending` — Search in customer username, email, status
- `ordering=-created_at` — Sort by field
- `page_size=20` — Items per page

**Response (Success - Lightweight List):**
```json
{
  "count": 287,
  "next": "http://localhost:8000/api/orders/?page=2",
  "previous": null,
  "results": [
    {
      "id": 42,
      "customer_name": "Chidi Okonkwo",
      "status": "delivered",
      "total_price": "234.99",
      "items_count": 3,
      "created_at": "2025-03-18T15:30:00Z"
    }
  ]
}
```

#### Get Order Details
```
GET /api/orders/{id}/
```

**Response (Success - Full Details):**
```json
{
  "id": 42,
  "customer_name": "Chidi Okonkwo",
  "customer_email": "chidi@example.com",
  "status": "delivered",
  "total_price": "234.99",
  "items_count": 3,
  "total_items": 5,
  "items": [
    {
      "id": 101,
      "product_name": "Ankara Dress",
      "artisan_name": "Amara Okafor",
      "quantity": 2,
      "price": "45.99",
      "subtotal": 91.98,
      "created_at": "2025-03-18T15:30:00Z"
    },
    {
      "id": 102,
      "product_name": "Beaded Necklace",
      "artisan_name": "Zainab Hassan",
      "quantity": 1,
      "price": "67.50",
      "subtotal": 67.50,
      "created_at": "2025-03-18T15:30:00Z"
    }
  ],
  "created_at": "2025-03-18T15:30:00Z",
  "updated_at": "2025-03-20T10:15:00Z"
}
```

#### Orders by Status
```
GET /api/orders/by_status/?status=pending
```

**Valid Status Values:**
- `pending` — Order awaiting confirmation
- `confirmed` — Order confirmed by seller
- `processing` — Order being prepared
- `shipped` — Order on the way
- `delivered` — Order delivered
- `cancelled` — Order cancelled

**Response:** Same as list endpoint (paginated list of orders).

---

### 5. REVIEWS (Artisan Ratings)

#### List Reviews
```
GET /api/reviews/
```

**Query Parameters:**
- `search=excellent` — Search in artisan username, rater username, comment
- `ordering=-rating` — Sort by field
- `page_size=20` — Items per page

**Response (Success):**
```json
{
  "count": 156,
  "next": "http://localhost:8000/api/reviews/?page=2",
  "previous": null,
  "results": [
    {
      "id": 28,
      "artisan_name": "Amara Okafor",
      "rater_username": "chidi_okonkwo",
      "rater_name": "Chidi Okonkwo",
      "rating": 5,
      "rating_display": "⭐⭐⭐⭐⭐ Excellent",
      "comment": "Excellent quality and fast shipping! Will definitely order again.",
      "created_at": "2025-03-18T08:45:00Z",
      "updated_at": "2025-03-18T08:45:00Z"
    },
    {
      "id": 27,
      "artisan_name": "Kofi Mensah",
      "rater_username": "fatima_ali",
      "rater_name": "Fatima Ali",
      "rating": 4,
      "rating_display": "⭐⭐⭐⭐ Very Good",
      "comment": "Great work, though shipping took a bit longer than expected.",
      "created_at": "2025-03-17T14:20:00Z",
      "updated_at": "2025-03-17T14:20:00Z"
    }
  ]
}
```

#### Get Review Details
```
GET /api/reviews/{id}/
```

Returns a single review object with full details.

---

## Pagination Format

All list endpoints return paginated responses:

```json
{
  "count": 156,
  "next": "http://localhost:8000/api/products/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      ...
    }
  ]
}
```

**Fields:**
- `count` — Total number of items across all pages
- `next` — URL to next page (null if on last page)
- `previous` — URL to previous page (null if on first page)
- `results` — Array of items for current page

---

## Query Examples

### Search Products
```
GET /api/products/?search=ankara
```

### Get Featured Products (Page 2)
```
GET /api/products/featured/?page=2&page_size=50
```

### Get Artisan's Products
```
GET /api/artisans/5/products/?page=1
```

### Get Pending Orders
```
GET /api/orders/by_status/?status=pending
```

### Search Artisans by Username
```
GET /api/artisans/?search=amara&ordering=username
```

### Get Top-Rated Reviews
```
GET /api/reviews/?ordering=-rating&page_size=10
```

---

## Error Responses

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 400 Bad Request
```json
{
  "error": "status query parameter is required"
}
```

### 500 Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK — Request successful |
| 400 | Bad Request — Invalid query parameters |
| 404 | Not Found — Resource doesn't exist |
| 500 | Server Error — Internal error |

---

## Best Practices

1. **Always paginate** — Use `page` parameter to avoid loading entire datasets
2. **Use `page_size`** — Adjust based on your needs (default 20, max 100)
3. **Filter data** — Use status filters, category filters to reduce payload
4. **Search efficiently** — Use search filters on client to find specific items
5. **Cache responses** — Cache stable data like categories and artisan info
6. **Handle pagination** — Follow `next` and `previous` URLs for pagination

---

## Integration Examples

### Python (Requests)
```python
import requests

# Get all products
response = requests.get('http://localhost:8000/api/products/')
products = response.json()['results']

# Search products
response = requests.get('http://localhost:8000/api/products/', params={
    'search': 'ankara',
    'page_size': 50
})

# Get product by ID
response = requests.get('http://localhost:8000/api/products/1/')
product = response.json()

# Get pending orders
response = requests.get('http://localhost:8000/api/orders/by_status/', params={
    'status': 'pending'
})
```

### JavaScript (Fetch)
```javascript
// Get products
fetch('http://localhost:8000/api/products/')
  .then(response => response.json())
  .then(data => console.log(data.results));

// Search artisans
fetch('http://localhost:8000/api/artisans/?search=kofi')
  .then(response => response.json())
  .then(data => console.log(data.results));

// Get artisan's products
fetch('http://localhost:8000/api/artisans/5/products/')
  .then(response => response.json())
  .then(data => console.log(data.results));
```

### cURL
```bash
# List products
curl http://localhost:8000/api/products/

# Get product by ID
curl http://localhost:8000/api/products/1/

# Search products
curl "http://localhost:8000/api/products/?search=ankara"

# Get pending orders
curl "http://localhost:8000/api/orders/by_status/?status=pending"
```

---

## Browsable API

Visit any endpoint in your browser to see the interactive API interface:
- `http://localhost:8000/api/products/`
- `http://localhost:8000/api/artisans/`
- `http://localhost:8000/api/categories/`
- `http://localhost:8000/api/orders/`
- `http://localhost:8000/api/reviews/`

---

## Future Enhancements

- Authentication (JWT/Token-based)
- Create/Update/Delete endpoints
- Rate limiting
- CORS configuration
- Filtering by price range
- Export to CSV
- Advanced analytics endpoints

