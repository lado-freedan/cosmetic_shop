"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.http import HttpResponse


def home_page(reuest):
    html_content = """
    <div style="font-family: sans-serif; text-align: center; margin-top: 100px">
        <h1 style="color: #4A5568;">Cosmetic ShopAPI</h1>
        <p style="color: #718096; font-size: 18px;">The Backend Server is Up and running successfully!</p>
        <div style="margin-top: 20px;">
            <a href="/api/products/" style="color: #3182CE; text-decoration: none; font-weight: bold;">View Products API</a>
        </div>
    </div>
    """
    return HttpResponse(html_content)

urlpatterns = [
    path("", home_page),
    path('admin/', admin.site.urls),
    path('api/products/', include('products.urls')),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/orders/", include("orders.urls")),
    path("api/users/", include("users.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
