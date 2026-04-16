from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.http import HttpResponseForbidden, JsonResponse
from .models import Product, Category, ArtisanRating
from .forms import ProductForm, ArtisanProfileForm, ArtisanBioForm, ArtisanRatingForm
from .currency_utils import get_active_currencies

User = get_user_model()


# ===== CURRENCY SELECTION =====

def set_currency(request, currency_code):
    """
    Set the user's selected currency in the session.
    Can be called via AJAX or regular redirect.
    """
    # Validate currency code
    currencies = get_active_currencies()
    valid_codes = [c.currency_code for c in currencies]
    
    if currency_code not in valid_codes:
        currency_code = 'USD'
    
    # Store in session
    request.session['selected_currency'] = currency_code
    request.session.modified = True
    
    # Return JSON if AJAX, else redirect
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success', 'currency': currency_code})
    
    # Redirect to referer or home
    return redirect(request.META.get('HTTP_REFERER', 'home'))


# ===== PUBLIC VIEWS =====

class ProductListView(ListView):
    """
    Display all products on the shop page.
    """
    model = Product
    template_name = 'products/shop.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Product.objects.select_related('category', 'artisan').all()
        artisan_id = self.request.GET.get('artisan')
        if artisan_id:
            queryset = queryset.filter(artisan_id=artisan_id)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        artisan_id = self.request.GET.get('artisan')
        if artisan_id:
            try:
                artisan = User.objects.get(id=artisan_id, is_artisan=True)
                context['filtered_artisan'] = artisan
            except User.DoesNotExist:
                pass
        return context


product_list = ProductListView.as_view()


class ProductDetailView(DetailView):
    """
    Display detailed information about a single product.
    """
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    
    def get_queryset(self):
        return Product.objects.select_related('category', 'artisan')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_products'] = Product.objects.filter(
            category=self.object.category
        ).exclude(id=self.object.id)[:4]
        return context


product_detail = ProductDetailView.as_view()


def category_products(request, category_id):
    """
    Display all products in a specific category.
    """
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category).select_related('artisan')
    categories = Category.objects.all()
    
    context = {
        'category': category,
        'products': products,
        'categories': categories,
    }
    return render(request, 'products/category.html', context)


def search_products(request):
    """
    Search products by name and description.
    """
    query = request.GET.get('q', '')
    products = []
    
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        ).select_related('category', 'artisan')
    
    categories = Category.objects.all()
    
    context = {
        'query': query,
        'products': products,
        'categories': categories,
    }
    return render(request, 'products/search_results.html', context)


def artisan_listing(request):
    """
    Display all artisans and their products - PUBLIC PAGE.
    Allows customers to browse and view artisan profiles.
    """
    # Get all artisans (users with is_artisan=True) with their profiles
    artisans = User.objects.filter(is_artisan=True).prefetch_related(
        'products',
        'artisanprofile'  # Use lowercase - Django's default related_name for OneToOneField
    )
    
    # Create a list of artisans with their product count and featured products
    artisan_data = []
    for artisan in artisans:
        products = artisan.products.all()
        
        # Get the artisan profile safely
        profile = None
        try:
            profile = artisan.artisanprofile
        except:
            pass
        
        artisan_info = {
            'user': artisan,
            'profile': profile,
            'product_count': products.count(),
            'featured_products': products[:3],  # Show up to 3 featured products
            'products': products
        }
        artisan_data.append(artisan_info)
    
    context = {
        'artisans': artisan_data,
        'total_artisans': len(artisan_data),
    }
    return render(request, 'products/artisan_listing.html', context)


def artisan_detail(request, artisan_id):
    """
    Display detailed profile of a single artisan.
    Shows profile information, bio, all products, and contact details.
    Allows users to rate the artisan.
    """
    # Get the artisan user
    artisan = get_object_or_404(User, id=artisan_id, is_artisan=True)
    
    # Get artisan profile - ensure it exists
    profile = None
    try:
        # Try to get the profile
        profile = artisan.artisanprofile
        # If it doesn't exist, Django will raise an exception
    except:
        # Profile doesn't exist, create one
        from accounts.models import ArtisanProfile
        profile = ArtisanProfile.objects.create(user=artisan)
    
    # Get all products from this artisan ordered by newest first
    products = Product.objects.filter(artisan=artisan).order_by('-created_at')
    
    # Get sales data
    from orders.models import OrderItem
    artisan_sales = OrderItem.objects.filter(artisan=artisan)
    total_sales = sum(item.price * item.quantity for item in artisan_sales)
    total_items_sold = sum(item.quantity for item in artisan_sales)
    
    # Get ratings
    ratings = ArtisanRating.objects.filter(artisan=artisan).order_by('-created_at')
    user_rating = None
    rating_form = None
    
    if request.user.is_authenticated and request.user != artisan:
        # Check if user has already rated this artisan
        user_rating = ArtisanRating.objects.filter(artisan=artisan, rater=request.user).first()
        
        if request.method == 'POST':
            form = ArtisanRatingForm(request.POST, instance=user_rating)
            if form.is_valid():
                rating_obj = form.save(commit=False)
                rating_obj.artisan = artisan
                rating_obj.rater = request.user
                rating_obj.save()
                user_rating = rating_obj
                messages.success(request, 'Thank you for rating!')
                ratings = ArtisanRating.objects.filter(artisan=artisan).order_by('-created_at')
            rating_form = form
        else:
            rating_form = ArtisanRatingForm(instance=user_rating) if user_rating else ArtisanRatingForm()
    
    context = {
        'artisan': artisan,
        'profile': profile,
        'products': products,
        'product_count': products.count(),
        'total_sales': total_sales,
        'total_items_sold': total_items_sold,
        'customer_count': artisan_sales.values('order__customer').distinct().count(),
        'has_profile_picture': profile and profile.profile_picture,
        'ratings': ratings,
        'user_rating': user_rating,
        'rating_form': rating_form,
        'average_rating': profile.get_average_rating(),
        'total_ratings': profile.get_total_ratings(),
    }
    return render(request, 'products/artisan_detail.html', context)


# ===== ARTISAN DASHBOARD VIEWS =====

@login_required(login_url='login')
def artisan_dashboard(request):
    """
    Main dashboard for artisans to manage their products and profile.
    Only accessible by artisans (is_artisan=True).
    Shows all values in the artisan's preferred currency (default USD).
    """
    if not request.user.is_artisan:
        return HttpResponseForbidden("You must be an artisan to access this page.")
    
    products = Product.objects.filter(artisan=request.user)
    
    # Get artisan's preferred currency (default to USD) - force fresh from database
    artisan_currency = 'USD'
    try:
        from accounts.models import ArtisanProfile
        artisan_profile = ArtisanProfile.objects.get(user=request.user)
        artisan_currency = artisan_profile.currency_preference or 'USD'
    except:
        pass
    
    # Import OrderItem to get sales data
    from orders.models import OrderItem
    from payments.models import ExchangeRate
    from products.currency_utils import get_currency_symbol
    
    artisan_order_items = OrderItem.objects.filter(artisan=request.user)
    orders_dict = {}
    for item in artisan_order_items:
        if item.order.id not in orders_dict:
            orders_dict[item.order.id] = item.order
    orders = list(orders_dict.values())
    
    total_sales = sum(item.price * item.quantity for item in artisan_order_items)
    total_inventory_value = sum(p.price * p.stock_quantity for p in products)
    
    # Helper function to convert any currency to artisan's currency
    def convert_price(amount, from_currency, to_currency):
        if from_currency == to_currency:
            return float(amount)
        try:
            # Get exchange rates for both currencies
            from_rate = ExchangeRate.objects.filter(
                currency__currency_code=from_currency
            ).latest('date_updated')
            to_rate = ExchangeRate.objects.filter(
                currency__currency_code=to_currency
            ).latest('date_updated')
            # Convert: amount * (from_rate / to_rate)
            converted = float(amount) * (float(from_rate.rate_to_usd) / float(to_rate.rate_to_usd))
            return round(converted, 2)
        except:
            return float(amount)
    
    # Helper function specifically for USD to artisan's currency
    def convert_to_artisan_currency(usd_amount):
        if artisan_currency == 'USD':
            return float(usd_amount)
        return convert_price(usd_amount, 'USD', artisan_currency)
    
    # Add converted prices to products for display
    for product in products:
        product.display_price = convert_price(product.price, product.currency_code, artisan_currency)
    
    context = {
        'products': products,
        'artisan_profile': artisan_profile,
        'artisan_currency': artisan_currency,
        'currency_symbol': get_currency_symbol(artisan_currency),
        'total_products': products.count(),
        'total_value': convert_to_artisan_currency(total_inventory_value),
        'total_sales': convert_to_artisan_currency(total_sales),
        'total_items_sold': sum(item.quantity for item in artisan_order_items),
        'orders': orders,
    }
    return render(request, 'products/artisan_dashboard.html', context)


@login_required(login_url='login')
def add_product(request):
    """
    Allow artisans to add a new product.
    """
    if not request.user.is_artisan:
        return HttpResponseForbidden("You must be an artisan to add products.")
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.artisan = request.user
            product.save()
            messages.success(request, 'Product added successfully!')
            return redirect('products:artisan_dashboard')
    else:
        form = ProductForm()
    
    context = {'form': form, 'action': 'Add'}
    return render(request, 'products/add_edit_product.html', context)


@login_required(login_url='login')
def edit_product(request, product_id):
    """
    Allow artisans to edit their own products.
    """
    if not request.user.is_artisan:
        return HttpResponseForbidden("You must be an artisan to edit products.")
    
    product = get_object_or_404(Product, id=product_id)
    
    # Check if the product belongs to the current user
    if product.artisan != request.user:
        return HttpResponseForbidden("You can only edit your own products.")
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('products:artisan_dashboard')
    else:
        form = ProductForm(instance=product)
    
    context = {'form': form, 'product': product, 'action': 'Edit'}
    return render(request, 'products/add_edit_product.html', context)


@login_required(login_url='login')
def delete_product(request, product_id):
    """
    Allow artisans to delete their own products.
    """
    if not request.user.is_artisan:
        return HttpResponseForbidden("You must be an artisan to delete products.")
    
    product = get_object_or_404(Product, id=product_id)
    
    # Check if the product belongs to the current user
    if product.artisan != request.user:
        return HttpResponseForbidden("You can only delete your own products.")
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('products:artisan_dashboard')
    
    context = {'product': product}
    return render(request, 'products/confirm_delete_product.html', context)


@login_required(login_url='login')
def edit_artisan_profile(request):
    """
    Allow artisans to edit their profile information.
    """
    if not request.user.is_artisan:
        return HttpResponseForbidden("You must be an artisan to edit your profile.")
    
    try:
        artisan_profile = request.user.artisanprofile
    except:
        from accounts.models import ArtisanProfile
        artisan_profile = ArtisanProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        user_form = ArtisanProfileForm(request.POST, user=request.user)
        bio_form = ArtisanBioForm(request.POST, request.FILES, instance=artisan_profile)
        
        if user_form.is_valid() and bio_form.is_valid():
            user_form.save()
            bio_form.save()
            
            messages.success(request, 'Profile updated successfully!')
            return redirect('products:artisan_dashboard')
    else:
        user_form = ArtisanProfileForm(user=request.user)
        bio_form = ArtisanBioForm(instance=artisan_profile)
    
    context = {
        'user_form': user_form,
        'bio_form': bio_form,
        'artisan_profile': artisan_profile,
    }
    return render(request, 'products/edit_artisan_profile.html', context)


@login_required(login_url='accounts:login')
def artisan_orders(request):
    """
    Display all orders containing the artisan's products.
    Artisans can see orders made for their products by customers.
    """
    if not request.user.is_artisan:
        return HttpResponseForbidden("You must be an artisan to access this page.")
    
    from orders.models import OrderItem
    
    # Get all OrderItems where this artisan sold the product
    artisan_order_items = OrderItem.objects.filter(
        artisan=request.user
    ).select_related('order', 'product').order_by('-created_at')
    
    # Group by order to show each order once
    orders_dict = {}
    for item in artisan_order_items:
        if item.order.id not in orders_dict:
            orders_dict[item.order.id] = item.order
    
    orders = list(orders_dict.values())
    
    # Get summary stats
    total_sales = sum(item.price * item.quantity for item in artisan_order_items)
    total_items_sold = sum(item.quantity for item in artisan_order_items)
    
    context = {
        'orders': orders,
        'total_sales': total_sales,
        'total_items_sold': total_items_sold,
        'order_items_count': artisan_order_items.count(),
    }
    return render(request, 'orders/artisan_orders.html', context)


@login_required(login_url='accounts:login')
def artisan_products(request):
    """
    Display all products for the current artisan with search and filter.
    """
    if not request.user.is_artisan:
        return HttpResponseForbidden("You must be an artisan to access this page.")
    
    # Get all artisan's products
    products = Product.objects.filter(artisan=request.user).select_related('category').order_by('-created_at')
    
    # Search functionality
    search_query = request.GET.get('q', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )
    
    # Filter by category
    category_filter = request.GET.get('category', '')
    if category_filter:
        products = products.filter(category_id=category_filter)
    
    # Filter by availability
    stock_filter = request.GET.get('stock', '')
    if stock_filter == 'low':
        products = products.filter(stock_quantity__lt=5)
    elif stock_filter == 'out':
        products = products.filter(stock_quantity=0)
    elif stock_filter == 'in':
        products = products.filter(stock_quantity__gt=0)
    
    # Get all categories for dropdown
    categories = Category.objects.all()
    
    # Get summary stats
    total_products = Product.objects.filter(artisan=request.user).count()
    total_inventory_value = sum(p.price * p.stock_quantity for p in Product.objects.filter(artisan=request.user))
    
    context = {
        'products': products,
        'categories': categories,
        'search_query': search_query,
        'category_filter': category_filter,
        'stock_filter': stock_filter,
        'total_products': total_products,
        'total_inventory_value': total_inventory_value,
    }
    return render(request, 'products/artisan_products.html', context)

