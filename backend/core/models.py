from django.db import models

# Create your models here.
class Style(models.Model):
    class Category(models.TextChoices):
        KNOTLESS_BRAIDS = "Knotless_Braids", "knotless braids"
        BOHO_LOCS = "Boho_Locs", "boho locs"
        CORNROWS = "Cornrows", "cornrows"
        BOX_BRAIDS = "Box_Braids", "box braids"
        OTHER = "Other", "other"
        
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique = True, help_text="URL-friendly identifier, e.g 'knotless-braids medium-length'")
    category = models.CharField(max_length=30, choices=Category.choices, default=Category.OTHER)
    description = models.TextField()
    prep_required = models.TextField(help_text="What the client should do before their appointment")
    estimated_duration_minutes = models.PositiveIntegerField(help_text="Appointment duration in minutes")
    maintenance_guidelines = models.TextField(help_text="How the client should maintain their style")
    starting_price = models.DecimalField(max_digits=6, decimal_places=2)
    hero_image = models.ImageField(upload_to="styles/", blank=True, null=True, help_text="The main image for this style, displayed on the website")
    is_active = models.BooleanField(default=True, help_text="Uncheck to hide this style from the website without deleting it")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['name']
        
    def __str__(self):
        return self.name
    
class GalleryImage(models.Model):
    image = models.ImageField(upload_to="styles/gallery/")
    caption = models.CharField(max_length=200, blank=True)
    style = models.ForeignKey(
        Style, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="gallery_images",
        help_text="Optional: Link this photo to a specific style")
    is_featured = models.BooleanField(default=False, help_text="Check this box to feature this image on the homepage")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return self.caption or f"Gallery photo #{self.pk}"
    
from django.core.validators import MinValueValidator, MaxValueValidator
class Review(models.Model):
    client_name = models.CharField(max_length=100)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], help_text="Rating from 1 to 5")
    comment = models.TextField()
    style = models.ForeignKey(Style, on_delete=models.SET_NULL, null=True, blank=True, related_name="reviews")
    is_approved = models.BooleanField(default=False, help_text="Only approve reviews that are shown publicly")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-created_at"]
    
    def __str__(self):
        return f"{self.client_name} - {self.rating}\u2605"
    
class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        CANCELLED = "cancelled", "Cancelled"
        
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()
    client_phone = models.CharField(max_length=20, blank=True)
    style = models.ForeignKey(Style, on_delete=models.PROTECT, related_name="bookings")
    requested_datetime = models.DateTimeField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    notes = models.TextField(blank=True, help_text="Optional: Any additional information or requests from the client")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-requested_datetime"]
    
    def __str__(self):
        return f"{self.client_name} - {self.style.name} on {self.requested_datetime:%Y-%m-%d %H:%M}"