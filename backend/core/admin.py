from django.contrib import admin
from django.utils.html import format_html
from core.models import Style, GalleryImage , Review, Booking

@admin.register(Style)
class StyleAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'starting_price', 'estimated_duration_minutes', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['thumbnail_preview', 'caption', 'style', 'is_featured', 'uploaded_at']
    list_filter = ['style', 'is_featured', 'uploaded_at']
    search_fields = ['caption']
    
    def thumbnail_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 50px; border-radius: 4px;" />', obj.image.url)
        return "(no image)"
    
    thumbnail_preview.short_description = 'Preview'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'rating', 'style', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at', 'style']
    search_fields = ['client_name', 'comment']
    actions = ['approve_reviews']
    
    @admin.action(description='Approve selected reviews')
    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'style', 'status', 'created_at', 'requested_datetime']
    list_filter = ['status', 'style']
    search_fields = ['client_name', 'client_email', 'client_phone']
    date_hierarchy = 'requested_datetime'