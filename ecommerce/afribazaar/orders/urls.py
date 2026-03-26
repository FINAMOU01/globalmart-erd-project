from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('cart/',                              views.cart_view,         name='cart'),
    path('cart/add/<int:product_id>/',         views.add_to_cart,       name='add_to_cart'),
    path('cart/remove/<int:item_id>/',         views.remove_from_cart,  name='remove_from_cart'),
    path('cart/update/<int:item_id>/',         views.update_quantity,   name='update_quantity'),
    path('checkout/',                          views.checkout,          name='checkout'),
    path('confirmation/<int:order_id>/',       views.order_confirmation, name='order_confirmation'),
    path('history/',                           views.order_history,     name='order_history'),
]