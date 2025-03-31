# store/urls.py
from .views import signup_view
from django.urls import path
from . import views
from .api import phone_list_api


urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
     path('signup/', signup_view, name='signup'),
     path('my-orders/', views.my_orders, name='my_orders'),
path('remove-from-cart/', views.remove_from_cart, name='remove_from_cart'),
 path('api/phones/', phone_list_api, name='phone_list_api'),

]
