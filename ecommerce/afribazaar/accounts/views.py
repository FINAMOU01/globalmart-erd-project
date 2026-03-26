from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomerRegisterForm, ArtisanRegisterForm, UserLoginForm, CustomerProfileUpdateForm, ArtisanProfileUpdateForm
from .models import CustomerProfile, ArtisanProfile


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
            return redirect('accounts:customer_profile')
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
                    return redirect('accounts:customer_profile')
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
def artisan_profile_view(request):
    # Redirect to the functional artisan dashboard
    return redirect('products:artisan_dashboard')
