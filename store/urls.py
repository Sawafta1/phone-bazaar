# store/urls.py
from .views import signup_view
from django.urls import path
from . import views
from .views import suggest_phone_view
from .views import contact_us

from .api import phone_compare_api

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('signup/', signup_view, name='signup'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('remove-from-cart/', views.remove_from_cart, name='remove_from_cart'),
    path('api/phones/compare/', phone_compare_api, name='phone_compare_api'),
    path('suggest-phone/', suggest_phone_view, name='suggest_phone'),
    path('contact/', contact_us, name='contact'),


]
