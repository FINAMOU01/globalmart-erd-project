# Artisan Dashboard - Setup & Usage Guide

## ✅ What's Implemented

Your artisan dashboard is now fully functional with the following features:

### 1. **Dashboard Overview**
- **URL**: `/products/artisan/dashboard/`
- **View Stats**:
  - Total products listed
  - Inventory value (total product value in stock)
  - Total sales from orders
  
### 2. **Add Products**
- **URL**: `/products/artisan/add-product/`
- **Features**:
  - Product name, description, category
  - Price and stock quantity
  - Product image upload
  - Product attributes (JSON format for flexible fields)
  - Mark products as featured
  
### 3. **Manage Products**
- **View Products**: All products shown in table format on dashboard
- **Edit**: Click edit button to modify product details
- **Delete**: Remove products with confirmation
- **Status**: See stock levels at a glance

### 4. **View Orders**
- **URL**: `/products/artisan/orders/`
- **Features**:
  - See all orders containing your products
  - View customer details
  - Check order status (Pending, Confirmed, Processing, Shipped, Delivered, Cancelled)
  - Click "View" to see detailed order items

### 5. **Edit Profile**
- **URL**: `/products/artisan/edit-profile/`
- **Features**:
  - Update personal information
  - Add profile picture
  - Write your artisan bio
  - Add social media links (Instagram, Facebook)

## 🚀 How to Access

### For New Artisans:
1. Go to home page → "Register as Artisan"
2. Fill in registration details
3. You'll be automatically redirected to the dashboard

### For Existing Artisans:
1. Login with your credentials
2. You'll be redirected to the functional dashboard
3. Click "Add New Product" to start selling

## 📱 Navigation Menu

From anywhere in the artisan area, use the sidebar to navigate:
- 📊 **Dashboard** - Main overview page
- 📦 **Orders** - View customer orders
- ➕ **Add New Product** - Create new product listing
- 👤 **Edit Profile** - Update your information
- 🚪 **Logout** - Sign out

## 📊 Dashboard Statistics

Your dashboard header displays three key metrics:

```
┌─────────────────────────────────────────────────┐
│  Dashboard                                      │
│                                                 │
│  [Products]  [Inventory Value]  [Total Sales]  │
│      12            USD 4,500         USD 2,800 │
└─────────────────────────────────────────────────┘
```

## 🎯 Quick Actions

| Action | URL | Description |
|--------|-----|-------------|
| Add Product | `/products/artisan/add-product/` | Create new product |
| View Orders | `/products/artisan/orders/` | See all orders |
| Edit Profile | `/products/artisan/edit-profile/` | Update info |
| Dashboard | `/products/artisan/dashboard/` | Main page |

## 🔧 Technical Details

- **Framework**: Django 4.2.10
- **Database**: SQLite (development)
- **Frontend**: Bootstrap 5
- **Image Upload**: Supported for products and profile pictures
- **Authentication**: Django's built-in auth system

## 📝 Sample Test Data

Run this to create test orders:
```bash
python create_test_orders.py
```

This creates sample orders so you can see how the orders page works.

## 🐛 Troubleshooting

**Q: Can't add products?**
A: Make sure you're registered as an artisan and logged in.

**Q: Images not showing?**
A: Check that `MEDIA_ROOT` and `MEDIA_URL` are configured in settings.py

**Q: Can't see orders?**
A: Create test orders using `create_test_orders.py` script

---

**Last Updated**: March 26, 2026
**Status**: ✅ Fully Functional
