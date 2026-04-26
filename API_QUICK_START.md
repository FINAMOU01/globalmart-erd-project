# AfriBazaar REST API - Quick Start Guide

## 🚀 Getting Started

### Prerequisites
- Django 6.0.3
- Django REST Framework (already installed)
- PostgreSQL database (already configured)
- Python 3.8+

### Start the Server
```bash
cd ecommerce/afribazaar
python manage.py runserver 0.0.0.0:8000
```

The API will be available at: **http://localhost:8000/api/**

---

## 📍 API Root

Visit the API root to see all available endpoints:
```
GET http://localhost:8000/api/
```

---

## 🔍 Quick Examples

### 1. Get All Products
```bash
curl http://localhost:8000/api/products/
```

**With Pagination:**
```bash
curl "http://localhost:8000/api/products/?page=1&page_size=50"
```

**With Search:**
```bash
curl "http://localhost:8000/api/products/?search=dashiki"
```

**With Ordering:**
```bash
curl "http://localhost:8000/api/products/?ordering=-price"  # By price descending
curl "http://localhost:8000/api/products/?ordering=created_at"  # By date ascending
```

---

### 2. Get Single Product
```bash
curl http://localhost:8000/api/products/42/
```

Returns full details including nested artisan and category info.

---

### 3. Get Featured Products
```bash
curl http://localhost:8000/api/products/featured/
```

---

### 4. Get Products by Category
```bash
curl "http://localhost:8000/api/products/by_category/?category_id=4"
```

---

### 5. Get Products by Artisan
```bash
curl "http://localhost:8000/api/products/by_artisan/?artisan_id=14"
```

---

### 6. Get All Artisans
```bash
curl http://localhost:8000/api/artisans/
```

---

### 7. Get Artisan Details
```bash
curl http://localhost:8000/api/artisans/14/
```

Returns artisan info with profile and ratings stats.

---

### 8. Get Artisan's Products
```bash
curl http://localhost:8000/api/artisans/14/products/
```

---

### 9. Get Artisan's Ratings
```bash
curl http://localhost:8000/api/artisans/14/ratings/
```

---

### 10. Get All Categories
```bash
curl http://localhost:8000/api/categories/
```

---

### 11. Get All Orders
```bash
curl http://localhost:8000/api/orders/
```

**With Pagination:**
```bash
curl "http://localhost:8000/api/orders/?page=1&page_size=20"
```

---

### 12. Get Order Details
```bash
curl http://localhost:8000/api/orders/1/
```

Returns order with all items included.

---

### 13. Get Orders by Status
```bash
# Pending orders
curl "http://localhost:8000/api/orders/by_status/?status=pending"

# Confirmed orders
curl "http://localhost:8000/api/orders/by_status/?status=confirmed"

# Shipped orders
curl "http://localhost:8000/api/orders/by_status/?status=shipped"

# Delivered orders
curl "http://localhost:8000/api/orders/by_status/?status=delivered"

# Valid statuses: pending, confirmed, processing, shipped, delivered, cancelled
```

---

### 14. Get All Reviews
```bash
curl http://localhost:8000/api/reviews/
```

---

### 15. Get Review Details
```bash
curl http://localhost:8000/api/reviews/1/
```

---

## 📊 Response Format

All successful responses return HTTP 200 OK with JSON:

```json
{
  "count": 156,
  "next": "http://localhost:8000/api/products/?page=2",
  "previous": null,
  "results": [
    { /* item objects */ }
  ]
}
```

**Fields:**
- `count` - Total items across all pages
- `next` - URL to next page (null if last page)
- `previous` - URL to previous page (null if first page)
- `results` - Array of items on current page

---

## ❌ Error Responses

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

## 🔑 Query Parameters Reference

### Pagination
- `page=1` - Get specific page (default: 1)
- `page_size=50` - Items per page (default: 20, max: 100)

### Search
- `search=ankara` - Full-text search across indexed fields

### Ordering
- `ordering=field_name` - Sort ascending
- `ordering=-field_name` - Sort descending
- `ordering=-created_at` - Latest first
- `ordering=price` - Lowest price first

### Filtering
- `category_id=4` - Products in category 4
- `artisan_id=14` - Products by artisan 14
- `status=pending` - Orders with status pending

---

## 🐍 Python Integration

### Using Requests Library
```python
import requests
from pprint import pprint

# Get products
response = requests.get('http://localhost:8000/api/products/')
data = response.json()
pprint(data)

# Search products
response = requests.get('http://localhost:8000/api/products/', params={
    'search': 'dashiki',
    'page_size': 50
})
products = response.json()['results']
for product in products:
    print(f"{product['name']} - {product['formatted_price']}")

# Get single product
response = requests.get('http://localhost:8000/api/products/42/')
product = response.json()
print(f"Artisan: {product['artisan']['first_name']} {product['artisan']['last_name']}")
print(f"Category: {product['category']['name']}")
print(f"Price: {product['formatted_price']}")

# Get pending orders
response = requests.get('http://localhost:8000/api/orders/by_status/', params={
    'status': 'pending',
    'page_size': 100
})
orders = response.json()['results']
print(f"Found {len(orders)} pending orders")
```

---

## 🔗 JavaScript Integration

### Using Fetch API
```javascript
// Get products
fetch('http://localhost:8000/api/products/')
  .then(response => response.json())
  .then(data => {
    console.log(`Total products: ${data.count}`);
    data.results.forEach(product => {
      console.log(`${product.name} - ${product.formatted_price}`);
    });
  });

// Search products
fetch('http://localhost:8000/api/products/?search=dashiki')
  .then(response => response.json())
  .then(data => console.log(data.results));

// Get artisan details
fetch('http://localhost:8000/api/artisans/14/')
  .then(response => response.json())
  .then(artisan => {
    console.log(artisan.username);
    console.log(artisan.profile.bio);
    console.log(`Rating: ${artisan.profile.average_rating}/5`);
  });

// Get order with items
fetch('http://localhost:8000/api/orders/1/')
  .then(response => response.json())
  .then(order => {
    console.log(`Order #${order.id}`);
    console.log(`Customer: ${order.customer_name}`);
    console.log(`Status: ${order.status}`);
    order.items.forEach(item => {
      console.log(`  - ${item.product_name} x${item.quantity} = $${item.subtotal}`);
    });
  });
```

---

## 📱 Frontend Integration Example

### React Component
```jsx
import { useEffect, useState } from 'react';

function ProductList() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);

  useEffect(() => {
    fetch(`http://localhost:8000/api/products/?page=${page}`)
      .then(res => res.json())
      .then(data => {
        setProducts(data.results);
        setLoading(false);
      })
      .catch(error => console.error('Error:', error));
  }, [page]);

  if (loading) return <p>Loading...</p>;

  return (
    <div>
      <h1>Products</h1>
      {products.map(product => (
        <div key={product.id}>
          <h3>{product.name}</h3>
          <p>By: {product.artisan_name}</p>
          <p>Price: {product.formatted_price}</p>
          <button onClick={() => setPage(page + 1)}>Next</button>
        </div>
      ))}
    </div>
  );
}
```

---

## 🎯 Common Use Cases

### Get Recently Added Products
```bash
curl "http://localhost:8000/api/products/?ordering=-created_at&page_size=10"
```

### Find Verified Artisans
```bash
# List all artisans and manually filter (API returns all)
curl http://localhost:8000/api/artisans/
```

### Get Products in Price Range
```bash
# Search and filter in frontend
curl "http://localhost:8000/api/products/?ordering=price"
```

### Get Top-Rated Artisans
```bash
# List all and sort by rating in frontend
curl http://localhost:8000/api/artisans/
```

### Track Order Status
```bash
curl http://localhost:8000/api/orders/42/
```

### Get Customer Reviews
```bash
curl "http://localhost:8000/api/reviews/?ordering=-rating"
```

---

## 🔄 Pagination Navigation

All list endpoints support pagination. Example flow:

```bash
# Get first page
curl "http://localhost:8000/api/products/"

# Response includes "next" URL:
# "next": "http://localhost:8000/api/products/?page=2"

# Get second page
curl "http://localhost:8000/api/products/?page=2"

# Continue following "next" links until "next" is null
```

---

## ✅ Available Fields per Endpoint

### Product Fields
- id, name, price, currency_code, formatted_price, stock_quantity
- image, attributes, is_featured
- created_at, updated_at
- artisan (nested), category (nested)

### Artisan Fields
- id, username, email, first_name, last_name, is_artisan
- profile (nested: phone, address, bio, profile_picture, social_links, is_verified, currency_preference, average_rating, total_ratings)
- products_count

### Order Fields
- id, customer_name, customer_email, status
- total_price, items_count, total_items
- items (nested array)
- created_at, updated_at

### Review Fields
- id, artisan_name, rater_username, rater_name
- rating, rating_display, comment
- created_at, updated_at

---

## 🐛 Troubleshooting

### API Not Responding
```bash
# Check if server is running
curl http://localhost:8000/api/

# If 404, ensure api app is in INSTALLED_APPS in settings.py
# If 500, check server logs
```

### Pagination Not Working
```bash
# Use correct parameter names
curl "http://localhost:8000/api/products/?page=1&page_size=50"

# page_size default is 20, max is 100
```

### Search Not Finding Results
```bash
# Search is case-insensitive but requires exact fields
# Only searches in: name, description, username, email (depending on endpoint)

curl "http://localhost:8000/api/products/?search=dashiki"
```

### Getting 400 Bad Request
```bash
# Check query parameters
curl "http://localhost:8000/api/orders/by_status/?status=invalid"
# Valid statuses: pending, confirmed, processing, shipped, delivered, cancelled
```

---

## 📖 Full Documentation

For complete API documentation, see: [API_DOCUMENTATION.md](../API_DOCUMENTATION.md)

---

## 🚀 You're Ready!

Start integrating the API into your applications. All endpoints are live and ready to serve data.

