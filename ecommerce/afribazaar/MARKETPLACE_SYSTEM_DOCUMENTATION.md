# AfriBazaar Product & Marketplace System - Complete Documentation

## 📋 Table of Contents
1. [System Overview](#system-overview)
2. [Models Architecture](#models-architecture)
3. [Admin Panel](#admin-panel)
4. [Artisan Dashboard](#artisan-dashboard)
5. [Views & URLs](#views--urls)
6. [Templates](#templates)
7. [Forms](#forms)
8. [Styling](#styling)
9. [Database Setup](#database-setup)
10. [Sample Data](#sample-data)
11. [Usage Guide](#usage-guide)

---

## System Overview

AfriBazaar is an African cultural e-commerce platform that connects artisans with customers interested in authentic handcrafted products. The system allows:

- **Customers**: Browse, search, and view products
- **Artisans**: Manage their own product inventory and profiles
- **Admins**: Manage all products, categories, users, and artisan profiles

### Key Features
- ✅ Product browsing with category filtering
- ✅ Full-text search functionality
- ✅ Dynamic product attributes (JSON)
- ✅ Artisan profiles with social links
- ✅ Artisan dashboard for CRUD operations
- ✅ Responsive design with African-inspired colors
- ✅ Admin panel for complete control

---

## Models Architecture

### 1. CustomUser (Extended Django User)

```python
class CustomUser(AbstractUser):
    is_artisan = BooleanField(default=False)
    phone = CharField(max_length=20)
    country = CharField(max_length=100)
```

**Purpose**: Extends Django's built-in User model with artisan designation and location info.

**Fields**:
- `username`: Unique username
- `email`: Email address
- `password`: Hashed password
- `is_artisan`: Boolean flag for artisan verification
- `first_name`, `last_name`: User's full name
- `phone`: Contact phone number
- `country`: Country of origin
- `is_active`: Account status
- `date_joined`: Creation timestamp

---

### 2. ArtisanProfile (OneToOne with CustomUser)

```python
class ArtisanProfile(models.Model):
    user = OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = TextField()
    profile_image = ImageField(upload_to='artisans/')
    social_links = JSONField()  # {"instagram": "url", "facebook": "url"}
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
```

**Purpose**: Stores detailed profile information for artisans.

**Fields**:
- `user`: Reference to the CustomUser (one-to-one)
- `bio`: Artisan's biography/story
- `profile_image`: Profile picture
- `social_links`: JSON object with social media links
- `created_at`, `updated_at`: Timestamps

**JSON Example for social_links**:
```json
{
  "instagram": "https://instagram.com/artisan_name",
  "facebook": "https://facebook.com/artisan_name",
  "twitter": "https://twitter.com/artisan_name"
}
```

---

### 3. Category

```python
class Category(models.Model):
    name = CharField(max_length=200, unique=True)
    description = TextField()
    image = ImageField(upload_to='categories/')
    created_at = DateTimeField(auto_now_add=True)
```

**Purpose**: Organizes products into logical categories.

**Fields**:
- `name`: Category name (unique)
- `description`: Category description
- `image`: Category icon/image
- `created_at`: Creation timestamp

**Sample Categories**:
- Textiles & Fabrics
- Jewelry & Accessories
- Fashion & Clothing
- Home Décor
- Art & Crafts

---

### 4. Product

```python
class Product(models.Model):
    artisan = ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    name = CharField(max_length=300)
    description = TextField()
    price = DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = IntegerField(default=0)
    image = ImageField(upload_to='products/')
    attributes = JSONField(default=dict)  # {"color": "red", "size": "M"}
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    is_featured = BooleanField(default=False)
```

**Purpose**: Represents individual products on the marketplace.

**Fields**:
- `artisan`: ForeignKey to artisan (seller)
- `category`: ForeignKey to product category
- `name`: Product name
- `description`: Detailed product description
- `price`: Product price in USD
- `stock_quantity`: Available units
- `image`: Product image
- `attributes`: JSON for flexible attributes
- `is_featured`: Boolean for featured products
- `created_at`, `updated_at`: Timestamps

**JSON Example for attributes**:
```json
{
  "color": "Red",
  "size": "Medium",
  "material": "Ankara Cotton",
  "origin": "Ghana"
}
```

---

## Admin Panel

The admin panel allows superusers to manage all aspects of the platform.

### CustomUserAdmin
```python
@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'get_full_name', 'is_artisan', 'phone', 'country', 'date_joined')
    list_filter = ('is_artisan', 'date_joined', 'country')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone')
```

**Admin Capabilities**:
- Create/edit/delete users
- Assign artisan status
- Filter by artisan status, country, date joined
- Search by username, email, phone
- Bulk actions

### ArtisanProfileAdmin
```python
@admin.register(ArtisanProfile)
class ArtisanProfileAdmin(admin.ModelAdmin):
    list_display = ('get_artisan_name', 'get_artisan_country', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__first_name', 'user__last_name', 'user__username')
```

**Admin Capabilities**:
- Manage artisan profiles
- View/edit bio and social links
- Manage profile images
- Filter by date created/updated

### CategoryAdmin
```python
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_product_count', 'created_at')
    search_fields = ('name', 'description')
```

**Admin Capabilities**:
- Create/edit/delete categories
- View product count per category
- Upload category images
- Search by name/description

### ProductAdmin
```python
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_artisan_name', 'category', 'price', 'stock_quantity', 'is_featured', 'created_at', 'get_image_preview')
    list_filter = ('category', 'is_featured', 'created_at', 'price')
    search_fields = ('name', 'description', 'artisan__first_name')
```

**Admin Capabilities**:
- Create/edit/delete products (any product)
- Mark as featured
- Adjust pricing and stock
- Upload product images
- View image previews
- Filter by category, price, date created
- Search by name, description, artisan

---

## Artisan Dashboard

Artisans (users with `is_artisan=True`) have access to a dedicated dashboard.

### Dashboard Features

#### 1. Dashboard Overview (`/products/artisan/dashboard/`)
- View all products created by the artisan
- See total product count
- Calculate total inventory value
- Profile card with bio and profile image
- Quick access to add new products
- Table of products with edit/delete options

#### 2. Add Product (`/products/artisan/add-product/`)
- Form to create new product
- Required fields: name, description, category, price, stock quantity, image
- Optional fields: attributes (JSON), featured status
- Automatic artisan assignment

#### 3. Edit Product (`/products/artisan/edit-product/<id>/`)
- Modify existing product details
- Update image, price, stock
- Edit dynamic attributes
- Only accessible by product creator

#### 4. Delete Product (`/products/artisan/delete-product/<id>/`)
- Confirmation page before deletion
- Shows product preview
- Permanently removes product

#### 5. Edit Profile (`/products/artisan/edit-artisan-profile/`)
- Update personal information (name, email, phone, country)
- Add/update biography
- Upload profile image
- Update social media links (JSON)

---

## Views & URLs

### URL Structure

```
/products/shop/                          → Product list view
/products/product/<id>/                  → Product detail view
/products/category/<id>/                 → Category products view
/products/search/                        → Search results view

/products/artisan/dashboard/             → Artisan dashboard
/products/artisan/add-product/           → Add product form
/products/artisan/edit-product/<id>/     → Edit product form
/products/artisan/delete-product/<id>/   → Delete confirmation
/products/artisan/edit-profile/          → Edit profile form
```

### View Details

#### ProductListView (Class-Based View)
```python
class ProductListView(ListView):
    model = Product
    template_name = 'products/shop.html'
    paginate_by = 12
    context_object_name = 'products'
```
- Displays all products in a grid
- Paginated (12 per page)
- Includes category filters

#### ProductDetailView (Class-Based View)
```python
class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
```
- Shows full product information
- Displays dynamic attributes
- Shows related products

#### category_products (Function-Based View)
- Filters products by category
- URL: `/products/category/<category_id>/`

#### search_products (Function-Based View)
- Full-text search by name and description
- Query parameter: `q`
- URL: `/products/search/?q=search_term`

#### Artisan Dashboard Views (All login_required)
- `artisan_dashboard()`: Main dashboard
- `add_product()`: Create new product
- `edit_product(product_id)`: Edit existing product
- `delete_product(product_id)`: Delete product
- `edit_artisan_profile()`: Update profile

---

## Templates

### Base Template (`base.html`)
- Master template for all pages
- Navigation bar with search
- User menu (login/logout)
- Footer with social links
- Message display system

### Public Templates

#### shop.html
- **Route**: `/products/shop/`
- **Features**:
  - Hero section with search bar
  - Category sidebar filter
  - Product grid (12 per page)
  - Product cards with image, name, price
  - Stock status indicator

#### product_detail.html
- **Route**: `/products/product/<id>/`
- **Features**:
  - Large product image
  - Product information (name, price, category)
  - Artisan information card
  - Dynamic attributes display
  - Quantity selector
  - Add to cart button (for future checkout)
  - Related products section

#### category.html
- **Route**: `/products/category/<id>/`
- **Features**:
  - Category name and description
  - Filtered product grid
  - Same product card styling

#### search_results.html
- **Route**: `/products/search/?q=term`
- **Features**:
  - Search query display
  - Results count
  - Filtered product grid
  - "No results" message

### Artisan Templates (Login Required)

#### artisan_dashboard.html
- **Route**: `/products/artisan/dashboard/`
- **Features**:
  - Dashboard header with stats
  - Artisan profile card
  - Products table with edit/delete
  - Navigation sidebar
  - Add product button

#### add_edit_product.html
- **Route**: `/products/artisan/add-product/` or `/products/artisan/edit-product/<id>/`
- **Features**:
  - Product form
  - Image upload with preview
  - JSON attributes field
  - Featured checkbox
  - Form validation

#### edit_artisan_profile.html
- **Route**: `/products/artisan/edit-artisan-profile/`
- **Features**:
  - Personal information form
  - Bio textarea
  - Profile image upload
  - Social links JSON field

#### confirm_delete_product.html
- **Route**: `/products/artisan/delete-product/<id>/` (GET)
- **Features**:
  - Product preview
  - Confirmation button
  - Warning message

---

## Forms

### ProductForm (ModelForm)
```python
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price', 'stock_quantity', 'image', 'attributes', 'is_featured']
```

**Features**:
- Bootstrap CSS classes
- JSON validation for attributes
- File upload for images
- All required fields except attributes and featured

### ArtisanProfileForm (Custom Form)
```python
class ArtisanProfileForm(forms.Form):
    first_name = CharField()
    last_name = CharField()
    email = EmailField()
    phone = CharField()
    country = CharField()
```

**Features**:
- Handles both User and ArtisanProfile fields
- Saves to both models
- Bootstrap styling

### ArtisanBioForm (Custom Form)
```python
class ArtisanBioForm(forms.Form):
    bio = CharField(widget=Textarea())
    profile_image = ImageField()
    social_links = CharField(widget=Textarea())  # JSON
```

**Features**:
- JSON validation for social_links
- Image upload
- Optional all fields

---

## Styling

### Color Palette (African-Inspired)

```css
--color-terracotta: #C44A2F;    /* Warm earth tone */
--color-gold: #D4AF37;          /* Luxury accent */
--color-black: #1E1E1E;         /* Deep charcoal */
--color-cream: #F5F3EE;         /* Warm background */
--color-emerald: #1F7A6B;       /* African green */
```

### Key Styling Features
- Responsive bootstrap grid
- Product card hover animations
- Smooth transitions
- Custom CSS variables
- Mobile-first design
- Accessibility considerations

### Responsive Breakpoints
- **Desktop**: Full layout
- **Tablet (768px)**: Adjusted font sizes, stacked layout
- **Mobile (576px)**: Single column, optimized touch targets

---

## Database Setup

### 1. Create Migration Files
```bash
python manage.py makemigrations users
python manage.py makemigrations products
```

### 2. Apply Migrations
```bash
python manage.py migrate
```

### 3. Create Superuser
```bash
python manage.py createsuperuser
```

### 4. Load Sample Data (Optional)
```bash
python manage.py loaddata products/fixtures/sample_data.json
```

### 5. Collect Static Files
```bash
python manage.py collectstatic
```

---

## Sample Data

Sample data includes:
- **5 Artisans**: Kofi (Ghana), Amara (Senegal), Zainab (Nigeria), Kamau (Kenya)
- **5 Categories**: Textiles, Jewelry, Fashion, Home Décor, Art & Crafts
- **8 Products**: Kente cloth, Bogolan, Ankara dress, etc.

Each product has:
- Product name and detailed description
- Price and stock quantity
- Product image path
- Dynamic attributes (JSON)
- Featured status
- Associated artisan and category

### Sample Product Structure
```json
{
  "artisan": 2,
  "category": 1,
  "name": "Authentic Kente Cloth Fabric",
  "description": "Handwoven Kente cloth...",
  "price": "75.00",
  "stock_quantity": 15,
  "image": "products/kente_cloth.jpg",
  "attributes": {
    "color": "Multi-colored",
    "size": "2 yards",
    "material": "Cotton",
    "origin": "Ghana"
  },
  "is_featured": true
}
```

---

## Usage Guide

### For Customers

1. **Browse Products**
   - Go to `/products/shop/`
   - Use category sidebar to filter
   - Click on product for details

2. **Search**
   - Use search bar on any page
   - Enter product name or description
   - View results on search page

3. **View Details**
   - Click "View Details" on any product
   - See all attributes
   - Learn about artisan
   - View related products

### For Artisans

1. **Register Account**
   - Create account
   - Admin marks as `is_artisan=True`
   - Create profile (optional)

2. **Access Dashboard**
   - Login
   - Click "My Dashboard" in navbar
   - View all your products

3. **Add Product**
   - Click "Add Product"
   - Fill in all required fields
   - Add JSON attributes if needed
   - Upload product image
   - Submit form

4. **Edit Product**
   - Click edit button in dashboard
   - Modify any details
   - Save changes

5. **Delete Product**
   - Click delete button
   - Confirm on preview page
   - Product removed

6. **Update Profile**
   - Click "Edit Profile"
   - Update personal info
   - Add bio and profile image
   - Add social media links
   - Save changes

### For Admins

1. **Access Admin Panel**
   - Go to `/admin/`
   - Login with superuser credentials

2. **Manage Categories**
   - Create categories
   - Add descriptions and icons
   - View product counts

3. **Manage Products**
   - Create/edit/delete products
   - Mark as featured
   - Adjust pricing
   - View image previews

4. **Manage Users**
   - Create users
   - Mark as artisan
   - Edit user info
   - View user list

5. **Manage Artisan Profiles**
   - Edit bios
   - Manage profile images
   - Update social links

---

## Integration Checklist

- [x] Models created (CustomUser, ArtisanProfile, Category, Product)
- [x] Admin panel configured
- [x] Forms created
- [x] Views and URLs configured
- [x] Templates created (all 11 templates)
- [x] CSS styling with African colors
- [x] Sample data fixture created
- [x] Media files configuration
- [x] Static files configuration

---

## Important Notes

1. **Settings Configuration**: Make sure `AUTH_USER_MODEL = 'users.CustomUser'` in settings
2. **Media Files**: Configure `MEDIA_URL` and `MEDIA_ROOT` in settings
3. **Image Upload**: Ensure `placeholder` images exist before loading fixtures
4. **Pillow Required**: Install Pillow for image handling: `pip install Pillow`
5. **Bootstrap & Font Awesome**: CDN links included in base.html

---

## Common Issues & Solutions

### Issue: Images not loading
**Solution**: Check `MEDIA_URL` and `MEDIA_ROOT` in settings, ensure URLs are configured

### Issue: Static files not loading
**Solution**: Run `python manage.py collectstatic`, check `STATIC_URL` and `STATICFILES_DIRS`

### Issue: Form validation fails for JSON
**Solution**: Use valid JSON format, e.g., `{"key":"value"}` with double quotes

### Issue: Artisan cannot edit products
**Solution**: Verify product's artisan matches logged-in user, check permission logic in views

---

## Future Enhancements

- Shopping cart functionality
- Payment integration
- Order management system
- Product reviews and ratings
- Wishlist feature
- Email notifications
- Advanced analytics dashboard
- Mobile app
- Multi-language support
- Inventory management alerts

