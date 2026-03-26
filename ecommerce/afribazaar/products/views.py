from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Product, Category
from .forms import ProductForm, ArtisanProfileForm, ArtisanBioForm

User = get_user_model()


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
        return Product.objects.select_related('category', 'artisan').all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
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


# ===== ARTISAN DASHBOARD VIEWS =====

@login_required(login_url='login')
def artisan_dashboard(request):
    """
    Main dashboard for artisans to manage their products and profile.
    Only accessible by artisans (is_artisan=True).
    """
    if not request.user.is_artisan:
        return HttpResponseForbidden("You must be an artisan to access this page.")
    
    products = Product.objects.filter(artisan=request.user)
    artisan_profile = getattr(request.user, 'artisan_profile', None)
    
    context = {
        'products': products,
        'artisan_profile': artisan_profile,
        'total_products': products.count(),
        'total_value': sum(p.price * p.stock_quantity for p in products),
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
    
    artisan_profile = getattr(request.user, 'artisan_profile', None)
    
    if request.method == 'POST':
        user_form = ArtisanProfileForm(request.POST, user=request.user)
        bio_form = ArtisanBioForm(request.POST, request.FILES)
        
        if user_form.is_valid() and bio_form.is_valid():
            user_form.save()
            
            # Create or update artisan profile
            if not artisan_profile:
                artisan_profile = request.user.artisan_profile
            
            if bio_form.cleaned_data.get('bio'):
                artisan_profile.bio = bio_form.cleaned_data.get('bio')
            
            if bio_form.cleaned_data.get('profile_image'):
                artisan_profile.profile_image = bio_form.cleaned_data.get('profile_image')
            
            if bio_form.cleaned_data.get('social_links'):
                import json
                artisan_profile.social_links = json.loads(bio_form.cleaned_data.get('social_links'))
            
            artisan_profile.save()
            
            messages.success(request, 'Profile updated successfully!')
            return redirect('products:artisan_dashboard')
    else:
        user_form = ArtisanProfileForm(user=request.user)
        bio_form = ArtisanBioForm(initial={
            'bio': artisan_profile.bio if artisan_profile else '',
            'social_links': artisan_profile.social_links if artisan_profile else '',
        })
    
    context = {
        'user_form': user_form,
        'bio_form': bio_form,
        'artisan_profile': artisan_profile,
    }
    return render(request, 'products/edit_artisan_profile.html', context)

