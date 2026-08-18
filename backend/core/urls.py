from django.urls import include, path
from rest_framework.routers import DefaultRouter

from core.views import GalleryImageViewSet, StyleViewSet, health_check, ReviewViewSet, BookingViewSet

router = DefaultRouter()
router.register("styles", StyleViewSet, basename="style")
router.register("gallery", GalleryImageViewSet, basename="gallery-image")
router.register("reviews", ReviewViewSet, basename="review")
router.register("bookings", BookingViewSet, basename="booking")

urlpatterns = [
    path("health/", health_check, name="health_check"),
    path("", include(router.urls))
]