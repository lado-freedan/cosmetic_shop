from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ProductListView


router = DefaultRouter()
router.register(r'', ProductListView, basename="products")


urlpatterns = [
    path("", include(router.urls)),
]