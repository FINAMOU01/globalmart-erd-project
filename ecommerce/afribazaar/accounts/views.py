from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .forms import CustomerRegisterForm, ArtisanRegisterForm, UserLoginForm, CustomerProfileUpdateForm, ArtisanProfileUpdateForm
from .models import CustomerProfile, ArtisanProfile, Wallet
from orders.models import Order, Cart


def register_choice_view(request):
    """Display registration type choice page"""
    return render(request, 'accounts/register_choice.html')


def customer_register_view(request):
    if request.method == 'POST':
        form = CustomerRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            login(request, user)
            return redirect('accounts:customer_dashboard')
    else:
        form = CustomerRegisterForm()
    return render(request, 'accounts/customer_register.html', {'form': form})


def artisan_register_view(request):
    if request.method == 'POST':
        form = ArtisanRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            login(request, user)
            return redirect('products:artisan_dashboard')
    else:
        form = ArtisanRegisterForm()
    return render(request, 'accounts/artisan_register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'You are now logged in as {username}.')
                # Redirect based on role
                if user.role == 'customer':
                    return redirect('accounts:customer_dashboard')
                elif user.role == 'artisan':
                    return redirect('products:artisan_dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('accounts:login')


@login_required
def customer_profile_view(request):
    if request.method == 'POST':
        form = CustomerProfileUpdateForm(request.POST, request.FILES, instance=request.user.customerprofile)
        if form.is_valid():
            # Save first_name and last_name to User model
            request.user.first_name = request.POST.get('first_name', '')
            request.user.last_name = request.POST.get('last_name', '')
            request.user.save()
            
            # Save profile updates
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('accounts:customer_profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomerProfileUpdateForm(instance=request.user.customerprofile)
    
    context = {
        'form': form,
        'customer_profile': request.user.customerprofile
    }
    return render(request, 'accounts/customer_profile.html', context)


@login_required
def customer_dashboard_view(request):
    """
    Customer dashboard showing orders, profile, and account info.
    Only accessible by customers (non-artisans).
    """
    if request.user.is_artisan:
        return HttpResponseForbidden("Only customers can access this page. Use your artisan dashboard instead.")
    
    # Get customer's orders
    orders = Order.objects.filter(customer=request.user).prefetch_related(
        'items__product__artisan'
    ).order_by('-created_at')
    
    # Get customer's cart
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        cart = None
    
    # Calculate statistics
    total_orders = orders.count()
    total_spent = sum(order.total_price for order in orders)
    recent_orders = orders[:5]  # Get last 5 orders
    
    # Count orders by status
    pending_orders = orders.filter(status='pending').count()
    delivered_orders = orders.filter(status='delivered').count()
    
    context = {
        'total_orders': total_orders,
        'total_spent': total_spent,
        'pending_orders': pending_orders,
        'delivered_orders': delivered_orders,
        'recent_orders': recent_orders,
        'all_orders': orders,
        'cart': cart,
        'cart_items_count': cart.items_count if cart else 0,
    }
    return render(request, 'accounts/customer_dashboard.html', context)


@login_required
def artisan_profile_view(request):
    # Redirect to the functional artisan dashboard
    return redirect('products:artisan_dashboard')


@login_required
def artisan_wallet_dashboard(request):
    """
    Artisan wallet dashboard showing balance and transaction history.
    Only accessible by logged-in artisans.
    """
    # Check if user is an artisan
    if not request.user.is_artisan:
        return HttpResponseForbidden("Only artisans can access the wallet dashboard.")
    
    # Get or create wallet
    try:
        wallet = Wallet.objects.get(artisan=request.user)
    except Wallet.DoesNotExist:
        wallet = Wallet.objects.create(artisan=request.user)
    
    # Get last 10 transactions (ordered by newest first)
    transactions = wallet.transactions.all()[:10]
    
    context = {
        'wallet': wallet,
        'transactions': transactions,
    }
    return render(request, 'accounts/artisan_wallet.html', context)
