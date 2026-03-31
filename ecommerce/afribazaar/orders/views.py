from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .models import Order, OrderItem, Cart, CartItem
from products.models import Product


@login_required(login_url='accounts:login')
def artisan_orders(request):
    """
    Display all orders containing the artisan's products.
    Artisans can see orders made for their products by customers.
    """
    if not request.user.is_artisan:
        return HttpResponseForbidden("You must be an artisan to access this page.")
    
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
def order_detail(request, order_id):
    """
    Display details of a specific order.
    Artisans can only see orders containing their products.
    """
    order = get_object_or_404(Order, id=order_id)
    
    # Get all items from this order that belong to the current artisan
    order_items = OrderItem.objects.filter(
        order=order,
        artisan=request.user
    ).select_related('product')
    
    # Check if artisan has any items in this order
    if not order_items.exists() and request.user.is_artisan:
        return HttpResponseForbidden("You don't have items in this order.")
    
    # If not artisan, allow customers to see their own orders
    if not request.user.is_artisan and order.customer != request.user:
        return HttpResponseForbidden("You can only view your own orders.")
    
    context = {
        'order': order,
        'items': order_items if request.user.is_artisan else order.items.all(),
    }
    return render(request, 'orders/order_detail.html', context)


@login_required(login_url='accounts:login')
def customer_orders(request):
    """
    Display all orders made by the current customer.
    """
    if request.user.is_artisan:
        return HttpResponseForbidden("Customers only. Use the artisan orders page instead.")
    
    orders = Order.objects.filter(customer=request.user).select_related(
        'customer'
    ).prefetch_related('items__product__artisan').order_by('-created_at')
    
    context = {
        'orders': orders,
    }
    return render(request, 'orders/customer_orders.html', context)


# ===== SHOPPING CART VIEWS =====

@login_required(login_url='accounts:login')
@login_required(login_url='accounts:login')
def add_to_cart(request, product_id):
    """
    Add a product to the user's shopping cart.
    Creates cart if it doesn't exist.
    Increments quantity if product already in cart.
    """
    product = get_object_or_404(Product, id=product_id)
    
    # Get or create cart for current user
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Get or create cart item
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )
    
    # If item already existed, increment quantity
    if not item_created:
        # Check stock availability
        if cart_item.quantity < product.stock_quantity:
            cart_item.quantity += 1
            cart_item.save()
        else:
            messages.warning(request, f"Cannot add more {product.name}. Only {product.stock_quantity} available.")
            return redirect('orders:cart_view')
    
    messages.success(request, f"{product.name} added to cart!")
    
    # Redirect back to referring page or to cart
    # Check both POST data and GET parameters for 'next'
    next_url = request.POST.get('next') or request.GET.get('next') or 'orders:cart_view'
    return redirect(next_url)


@login_required(login_url='accounts:login')
def cart_view(request):
    """
    Display the user's shopping cart with all items.
    Shows quantities, prices, subtotals, and total.
    """
    try:
        cart = Cart.objects.prefetch_related('items__product').get(user=request.user)
        cart_items = cart.items.all()
    except Cart.DoesNotExist:
        cart = None
        cart_items = []
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': cart.total_price if cart else 0,
        'items_count': cart.items_count if cart else 0,
    }
    return render(request, 'cart/cart.html', context)


@login_required(login_url='accounts:login')
@require_http_methods(["POST"])
def remove_from_cart(request, item_id):
    """
    Remove an item from the user's shopping cart.
    """
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    
    messages.success(request, f"{product_name} removed from cart!")
    return redirect('orders:cart_view')


@login_required(login_url='accounts:login')
@require_http_methods(["POST"])
def update_quantity(request, item_id):
    """
    Update the quantity of an item in the shopping cart.
    Expects POST data with 'quantity' field.
    """
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    try:
        new_quantity = int(request.POST.get('quantity', 1))
        
        # Validate quantity
        if new_quantity < 1:
            messages.error(request, "Quantity must be at least 1.")
            return redirect('orders:cart_view')
        
        if new_quantity > cart_item.product.stock_quantity:
            messages.warning(
                request,
                f"Only {cart_item.product.stock_quantity} of {cart_item.product.name} available."
            )
            new_quantity = cart_item.product.stock_quantity
        
        cart_item.quantity = new_quantity
        cart_item.save()
        
        messages.success(request, "Cart updated!")
    except ValueError:
        messages.error(request, "Invalid quantity.")
    
    return redirect('orders:cart_view')


@login_required(login_url='accounts:login')
def checkout_view(request):
    """
    Process checkout: convert cart into an order and clear the cart.
    Creates an Order with status 'pending' and OrderItems for each CartItem.
    """
    # Get user's cart
    try:
        cart = Cart.objects.prefetch_related('items__product').get(user=request.user)
    except Cart.DoesNotExist:
        messages.error(request, "Your cart is empty.")
        return redirect('orders:cart_view')
    
    # Check if cart has items
    if not cart.items.exists():
        messages.error(request, "Your cart is empty. Add items before checkout.")
        return redirect('products:product_list')
    
    # Calculate total from cart items
    total_price = cart.total_price
    
    # Create Order with total price
    order = Order.objects.create(
        customer=request.user,
        status='pending',
        total_price=total_price
    )
    
    # Create OrderItems from CartItems
    cart_items = cart.items.all()
    for cart_item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            artisan=cart_item.product.artisan,  # Get artisan from product
            quantity=cart_item.quantity,
            price=cart_item.product.price
        )
        
        # Reduce product stock
        product = cart_item.product
        product.stock_quantity -= cart_item.quantity
        product.save()
    
    # Clear the cart
    cart_items.delete()
    
    messages.success(request, "Order placed successfully!")
    return redirect('orders:checkout_confirmation', order_id=order.id)


@login_required(login_url='accounts:login')
@require_http_methods(["POST"])
def checkout_single_item(request, item_id):
    """
    Checkout a single item from the cart.
    Creates an Order with just that one item and removes it from cart.
    """
    # Get the cart item
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product = cart_item.product
    
    # Check stock availability
    if cart_item.quantity > product.stock_quantity:
        messages.error(request, f"Insufficient stock for {product.name}.")
        return redirect('orders:cart_view')
    
    # Calculate total for this item
    item_total = cart_item.product.price * cart_item.quantity
    
    # Create Order with this item only
    order = Order.objects.create(
        customer=request.user,
        status='pending',
        total_price=item_total
    )
    
    # Create OrderItem from CartItem
    OrderItem.objects.create(
        order=order,
        product=product,
        artisan=product.artisan,
        quantity=cart_item.quantity,
        price=product.price
    )
    
    # Reduce product stock
    product.stock_quantity -= cart_item.quantity
    product.save()
    
    # Remove this item from cart
    cart_item.delete()
    
    messages.success(request, f"Proceeding to checkout for {product.name}!")
    return redirect('orders:checkout_confirmation', order_id=order.id)


@login_required(login_url='accounts:login')
def checkout_confirmation_view(request, order_id):
    """
    Display order confirmation details after successful checkout.
    """
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    
    context = {
        'order': order,
        'order_items': order.items.all(),
    }
    return render(request, 'orders/checkout_confirmation.html', context)
