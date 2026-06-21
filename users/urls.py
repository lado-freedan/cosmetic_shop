from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import RegisterView, AddressViewSet

router = DefaultRouter()
router.register(r"addresses", AddressViewSet, basename="address")

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("", include(router.urls)),
]