# phone_bazaar/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='store/auth.html'), name='login'),
path('logout/', auth_views.LogoutView.as_view(template_name='store/logged_out.html'), name='logout'),
    path('api/auth/', include('allauth.socialaccount.urls')),  # ✅ Google login
    path('api/auth/', include('dj_rest_auth.urls')),  # login/logout/password
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),  # signup

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
