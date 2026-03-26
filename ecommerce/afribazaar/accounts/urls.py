from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_choice_view, name='register'),
    path('register/customer/', views.customer_register_view, name='customer_register'),
    path('register/artisan/', views.artisan_register_view, name='artisan_register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/customer/', views.customer_profile_view, name='customer_profile'),
    path('profile/artisan/', views.artisan_profile_view, name='artisan_profile'),
]