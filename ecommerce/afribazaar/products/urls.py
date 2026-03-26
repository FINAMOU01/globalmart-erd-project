from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # Public views
    path('shop/', views.product_list, name='shop'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('category/<int:category_id>/', views.category_products, name='category'),
    path('search/', views.search_products, name='search'),
    
    # Artisan dashboard views
    path('artisan/dashboard/', views.artisan_dashboard, name='artisan_dashboard'),
    path('artisan/add-product/', views.add_product, name='add_product'),
    path('artisan/edit-product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('artisan/delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('artisan/edit-profile/', views.edit_artisan_profile, name='edit_artisan_profile'),
]
