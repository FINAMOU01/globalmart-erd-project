from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from .models import Cart, CartItem, Order, OrderItem


# ──────────────────────────────────────────
# HELPER — Get or create cart for logged-in user
# ──────────────────────────────────────────

def get_or_create_cart(user):
    """Always returns the user's cart, creating one if it doesn't exist yet."""
    cart, created = Cart.objects.get_or_create(user=user)
    return cart


# ──────────────────────────────────────────
# 1. VIEW CART
# ──────────────────────────────────────────

@login_required
def cart_view(request):
    """
    Displays the user's cart with all items and total.
    @login_required means only logged-in users can access this page.
    """
    cart  = get_or_create_cart(request.user)
    items = cart.items.select_related('product').all()

    context = {
        'cart' : cart,
        'items': items,
        'total': cart.get_total(),
    }
    return render(request, 'orders/cart.html', context)


# ──────────────────────────────────────────
# 2. ADD TO CART
# ──────────────────────────────────────────

@login_required
def add_to_cart(request, product_id):
    """
    Adds a product to the cart.
    If it's already in the cart, increases the quantity by 1.
    """
    product  = get_object_or_404(Product, id=product_id)
    cart     = get_or_create_cart(request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart    = cart,
        product = product,
        defaults = {'quantity': 1}
    )

    if not created:
        # Product already in cart — just increase quantity
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f'"{product.name}" added to cart!')
    return redirect('orders:cart')


# ──────────────────────────────────────────
# 3. REMOVE FROM CART
# ──────────────────────────────────────────

@login_required
def remove_from_cart(request, item_id):
    """
    Removes a specific item from the cart completely.
    """
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()

    messages.success(request, f'"{product_name}" removed from cart.')
    return redirect('orders:cart')


# ──────────────────────────────────────────
# 4. UPDATE QUANTITY
# ──────────────────────────────────────────

@login_required
def update_quantity(request, item_id):
    """
    Updates the quantity of a cart item.
    If quantity reaches 0, the item is removed automatically.
    """
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))

        if quantity <= 0:
            cart_item.delete()
            messages.success(request, 'Item removed from cart.')
        else:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Cart updated.')

    return redirect('orders:cart')


# ──────────────────────────────────────────
# 5. CHECKOUT
# ──────────────────────────────────────────

@login_required
def checkout(request):
    """
    GET  — shows the checkout form (shipping address).
    POST — converts the cart into a real Order.
    """
    cart  = get_or_create_cart(request.user)
    items = cart.items.select_related('product').all()

    if not items:
        messages.warning(request, 'Your cart is empty!')
        return redirect('orders:cart')

    if request.method == 'POST':
        shipping_address = request.POST.get('shipping_address', '').strip()

        if not shipping_address:
            messages.error(request, 'Please enter a shipping address.')
            return redirect('orders:checkout')

        # ── Create the Order ──────────────────────────
        order = Order.objects.create(
            customer         = request.user,
            shipping_address = shipping_address,
            status           = Order.Status.PENDING,
            total            = cart.get_total(),
        )

        # ── Copy each CartItem → OrderItem ────────────
        for item in items:
            OrderItem.objects.create(
                order    = order,
                product  = item.product,
                quantity = item.quantity,
                price    = item.product.price,  # snapshot price at checkout
            )

        # ── Clear the cart ────────────────────────────
        cart.items.all().delete()

        messages.success(request, f'Order #{order.id} placed successfully!')
        return redirect('orders:order_confirmation', order_id=order.id)

    context = {
        'cart' : cart,
        'items': items,
        'total': cart.get_total(),
    }
    return render(request, 'orders/checkout.html', context)


# ──────────────────────────────────────────
# 6. ORDER CONFIRMATION
# ──────────────────────────────────────────

@login_required
def order_confirmation(request, order_id):
    """
    Shows a summary of the order just placed.
    """
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    items = order.order_items.select_related('product').all()

    context = {
        'order': order,
        'items': items,
    }
    return render(request, 'orders/order_confirmation.html', context)


# ──────────────────────────────────────────
# 7. ORDER HISTORY
# ──────────────────────────────────────────

@login_required
def order_history(request):
    """
    Shows all past orders for the logged-in user.
    """
    orders = Order.objects.filter(
        customer=request.user
    ).prefetch_related('order_items__product')

    context = {'orders': orders}
    return render(request, 'orders/order_history.html', context)