from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # Order views
    path('artisan/orders/', views.artisan_orders, name='artisan_orders'),
    path('customer/orders/', views.customer_orders, name='customer_orders'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    
    # Shopping cart views
    path('cart/', views.cart_view, name='cart_view'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update/<int:item_id>/', views.update_quantity, name='update_quantity'),
    
    # Checkout views
    path('checkout/', views.checkout_view, name='checkout'),
    path('checkout/item/<int:item_id>/', views.checkout_single_item, name='checkout_single_item'),
    path('checkout/confirmation/<int:order_id>/', views.checkout_confirmation_view, name='checkout_confirmation'),
]
