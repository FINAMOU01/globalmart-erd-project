from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Order, OrderItem


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
