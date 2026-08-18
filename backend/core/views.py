from django.db.models.query import QuerySet
from rest_framework import mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from core.models import Booking, Review, Style, GalleryImage
from core.serializers import StyleSerializer, GalleryImageSerializer, ReviewSerializer, BookingSerializer

@api_view(["GET"])
def health_check(request):
    return Response({"status": "ok", "service": "braiding-website-api"})

# booking viewset for the frontend to create a new booking and get all bookings
class BookingViewSet(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()

# review viewset for the frontend to create a new review and get all approved reviews
class ReviewViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(is_approved=True)
 

    
# gallery image viewset for the frontend to get all gallery images and filter by style or featured
class GalleryImageViewSet(ReadOnlyModelViewSet):
    serializer_class = GalleryImageSerializer
    
    def get_queryset(self):
        queryset = GalleryImage.objects.all()
        style_id = self.request.query_params.get("style")
        if style_id:
            queryset = queryset.filter(style_id=style_id)
        featured_only = self.request.query_params.get("featured")
        if featured_only == "true":
            queryset = queryset.filter(is_featured=True)
        return queryset


    
#style viewset for the frontend to get all styles and filter by category
class StyleViewSet(ReadOnlyModelViewSet):
    serializer_class = StyleSerializer
    
    def get_queryset(self):
        queryset = Style.objects.filter(is_active=True)
        category = self.request.query_params.get("category") # type: ignore
        if category:
            queryset = queryset.filter(category=category)
        return queryset