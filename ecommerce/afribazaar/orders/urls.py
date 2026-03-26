from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('artisan/orders/', views.artisan_orders, name='artisan_orders'),
    path('customer/orders/', views.customer_orders, name='customer_orders'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
]
