from rest_framework import serializers
from datetime import timedelta
from core.models import Style, GalleryImage, Review, Booking

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            "id",
            "client_name",
            "client_email",
            "client_phone",
            "style",
            "requested_datetime",
            "status",
            "notes",
            "created_at",
        ]
        read_only_fields = ["status", "created_at"]
    
    def validate(self, attrs):
        style = attrs["style"]
        requested_start = attrs["requested_datetime"]
        requested_end = requested_start + timedelta(minutes=style.estimated_duration_minutes)

        active_bookings = Booking.objects.filter(status__in=[Booking.Status.PENDING, Booking.Status.CONFIRMED])
        for booking in active_bookings:
            existing_start = booking.requested_datetime
            existing_end = existing_start + timedelta(minutes=booking.style.estimated_duration_minutes)
            if requested_start < existing_end and existing_start < requested_end:
                raise serializers.ValidationError(
                    "This time slot overlaps with an existing booking. Please choose a different time."
                )
        return attrs

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            "id",
            "client_name",
            "rating",
            "comment",
            "style",
            "is_approved",
            "created_at",
        ]
        read_only_fields = ["is_approved", "created_at"]
        
        
class GalleryImageSerializer(serializers.ModelSerializer):
    style_name = serializers.CharField(source="style.name", read_only=True, default = None)
    
    class Meta:
        model = GalleryImage
        fields = [
            "id",
            "image",
            "caption",
            "style",
            "style_name",
            "is_featured",
            "uploaded_at",
        ]

class StyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Style
        fields = [
            "id",
            "name",
            "slug",
            "category",
            "description",
            "prep_required",
            "estimated_duration_minutes",
            "maintenance_guidelines",
            "starting_price",
            "hero_image",
            "is_active",
        ]