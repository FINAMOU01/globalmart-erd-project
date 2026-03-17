# AfriBazaar Quick Start Guide

## Installation & Setup (5 minutes)

### Step 1: Install Dependencies
```bash
pip install Pillow django-widget-tweaks
```

### Step 2: Update Django Settings
The settings have already been updated. Verify:
```python
# afribazaar/settings.py
AUTH_USER_MODEL = 'users.CustomUser'
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### Step 3: Create Migrations
```bash
python manage.py makemigrations users
python manage.py makemigrations products
```

### Step 4: Apply Migrations
```bash
python manage.py migrate
```

### Step 5: Create Superuser
```bash
python manage.py createsuperuser
```

### Step 6: Load Sample Data (Optional)
```bash
python manage.py loaddata products/fixtures/sample_data.json
```

### Step 7: Create Media Directories
```bash
mkdir -p media/products
mkdir -p media/artisans
mkdir -p media/categories
```

### Step 8: Run Development Server
```bash
python manage.py runserver
```

---

## Access Points

### Admin Panel
**URL**: `http://localhost:8000/admin/`
- Username: (your superuser username)
- Password: (your superuser password)

### Shop Page
**URL**: `http://localhost:8000/products/shop/`
- Browse all products
- Use category filters
- Search for products

### Artisan Dashboard (After login)
**URL**: `http://localhost:8000/products/artisan/dashboard/`
- Manage your products
- Edit profile
- Add new products

---

## Quick Test Flow

### As Admin
1. Go to `/admin/`
2. Create a new user and mark as `is_artisan=True`
3. Create categories
4. Verify all models in admin panel

### As Artisan
1. Go to `/auth/login/` (create simple login if needed)
2. Login with artisan account
3. Go to `/products/artisan/dashboard/`
4. Add a new product
5. View on `/products/shop/`

### As Customer
1. Go to `/products/shop/`
2. Browse products
3. Search using search bar
4. Filter by category
5. Click product for details

---

## Files Created/Modified

### Models
- ✅ `users/models.py` - CustomUser, ArtisanProfile
- ✅ `products/models.py` - Category, Product

### Admin
- ✅ `users/admin.py` - User and Artisan admin
- ✅ `products/admin.py` - Category and Product admin

### Views
- ✅ `products/views.py` - All views for shop, artisan dashboard

### Forms
- ✅ `products/forms.py` - ProductForm, ArtisanProfileForm

### URLs
- ✅ `products/urls.py` - Product URLs
- ✅ `users/urls.py` - User auth URLs
- ✅ `afribazaar/urls.py` - Main URL configuration

### Templates (11 files)
- ✅ `templates/base.html` - Base template with navbar
- ✅ `templates/products/shop.html` - Product list
- ✅ `templates/products/product_detail.html` - Product detail
- ✅ `templates/products/category.html` - Category products
- ✅ `templates/products/search_results.html` - Search results
- ✅ `templates/products/artisan_dashboard.html` - Artisan dashboard
- ✅ `templates/products/add_edit_product.html` - Product form
- ✅ `templates/products/edit_artisan_profile.html` - Profile form
- ✅ `templates/products/confirm_delete_product.html` - Delete confirmation

### Styling
- ✅ `static/css/style.css` - Complete African-themed styling

### Data
- ✅ `products/fixtures/sample_data.json` - Sample products and artisans

### Documentation
- ✅ `MARKETPLACE_SYSTEM_DOCUMENTATION.md` - Full documentation
- ✅ `QUICK_START.md` - This file

---

## Key Features Implemented

### ✨ Public Features
- [x] Browse all products with images
- [x] Filter by category
- [x] Full-text search
- [x] Product detail pages with artisan info
- [x] Dynamic product attributes (JSON)
- [x] Responsive grid layout
- [x] Stock status indicators

### 🎨 Artisan Features
- [x] Secure login/logout
- [x] Dashboard with product management
- [x] Add new products
- [x] Edit existing products
- [x] Delete products
- [x] Manage artisan profile
- [x] Upload profile image
- [x] Add social media links
- [x] View product inventory value

### 🔧 Admin Features
- [x] Complete user management
- [x] Artisan verification
- [x] Category management
- [x] Product moderation
- [x] Feature product capability
- [x] Bulk actions
- [x] Advanced filtering
- [x] Search functionality

### 🎨 Design Features
- [x] African-inspired color palette
- [x] Responsive Bootstrap layout
- [x] Smooth animations and transitions
- [x] Product card hover effects
- [x] Professional typography
- [x] Mobile-optimized
- [x] Accessibility features

---

## Customization Guide

### Change Colors
Edit `static/css/style.css`:
```css
:root {
    --color-terracotta: #C44A2F;    /* Change here */
    --color-gold: #D4AF37;          /* Change here */
    --color-emerald: #1F7A6B;       /* Change here */
}
```

### Modify Product Fields
1. Edit model in `products/models.py`
2. Create migration: `python manage.py makemigrations`
3. Apply migration: `python manage.py migrate`
4. Update form in `products/forms.py`
5. Update template in `templates/products/add_edit_product.html`

### Add Authentication
Currently using Django's default login. To add custom auth:
1. Create `users/views.py` with registration view
2. Add URLs to `users/urls.py`
3. Create registration template
4. Link in navbar

### Products Per Page
In `products/views.py`, change `ProductListView`:
```python
paginate_by = 12  # Change this number
```

---

## Troubleshooting

### Migration Errors
```bash
# Reset migrations (for development only)
python manage.py migrate users zero
python manage.py migrate products zero
python manage.py makemigrations
python manage.py migrate
```

### Image Upload Issues
- Ensure `media/` directory exists
- Check file permissions
- Verify Pillow is installed: `pip install Pillow`

### Static Files Not Loading
```bash
python manage.py collectstatic --noinput
```

### Login Always Redirects
- Ensure `LOGIN_URL` is set in settings
- Check artisan dashboard login_required decorator

---

## Testing Checklist

- [ ] Create superuser
- [ ] Login to admin
- [ ] Create categories
- [ ] Create artisan user
- [ ] Create artisan profile
- [ ] Login as artisan
- [ ] Add product
- [ ] View shop page
- [ ] Filter by category
- [ ] Search for product
- [ ] View product detail
- [ ] Edit artisan profile
- [ ] Edit product
- [ ] Delete product

---

## Performance Tips

1. **Enable Django Debug Toolbar**
   ```bash
   pip install django-debug-toolbar
   ```

2. **Use select_related() and prefetch_related()**
   - Already implemented in views

3. **Cache Categories**
   - Use Django cache framework

4. **Optimize Images**
   - Recommend max 2MB per image

5. **Use CDN for Static Files**
   - Consider Cloudinary or AWS S3

---

## Security Considerations

- ✅ CSRF protection enabled
- ✅ Login required for artisan dashboard
- ✅ Artisan can only edit own products
- ✅ Admin only operations protected
- ✅ Form validation implemented
- ⚠️ TODO: Add SSL/HTTPS in production
- ⚠️ TODO: Add rate limiting
- ⚠️ TODO: Sanitize JSON input

---

## Next Steps

1. **Add Login/Registration Views**
   - Implement custom registration
   - Add email verification

2. **Implement Shopping Cart**
   - Create Cart model
   - Add to cart functionality
   - Cart page template

3. **Add Checkout & Payments**
   - Integration with Stripe/PayPal
   - Order creation
   - Order tracking

4. **Add Reviews & Ratings**
   - Create Review model
   - Review display on product detail
   - Artisan rating system

5. **Add Email Notifications**
   - Order confirmation
   - Profile update notifications
   - New product alerts

---

## Project Structure Reference

```
afribazaar/
├── afribazaar/              # Main project settings
│   ├── settings.py          # ✅ Updated with custom user
│   ├── urls.py              # ✅ Updated with includes
│   └── ...
├── users/                   # User management app
│   ├── models.py            # ✅ CustomUser, ArtisanProfile
│   ├── admin.py             # ✅ User admin
│   ├── urls.py              # ✅ Auth URLs
│   └── forms.py             # TODO: Registration form
├── products/                # Products app
│   ├── models.py            # ✅ Category, Product
│   ├── admin.py             # ✅ Product admin
│   ├── views.py             # ✅ All views
│   ├── urls.py              # ✅ Product URLs
│   ├── forms.py             # ✅ Product forms
│   └── fixtures/            # ✅ Sample data
├── templates/               # All templates
│   ├── base.html            # ✅ Base template
│   └── products/            # ✅ 9 product templates
├── static/                  # Static files
│   └── css/
│       └── style.css        # ✅ Comprehensive styling
└── media/                   # User uploads
    ├── products/
    ├── artisans/
    └── categories/
```

---

## Support & Resources

- Django Docs: https://docs.djangoproject.com/
- Django Models: https://docs.djangoproject.com/en/stable/topics/db/models/
- JSONField: https://docs.djangoproject.com/en/stable/topics/db/models/fields/#json-field
- Bootstrap 5: https://getbootstrap.com/docs/5.3/
- Font Awesome: https://fontawesome.com/

---

**🎉 Congratulations!** Your AfriBazaar marketplace is ready to go!

For detailed documentation, see: `MARKETPLACE_SYSTEM_DOCUMENTATION.md`
