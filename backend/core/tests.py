from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase

from core.models import Booking, GalleryImage, Review, Style


def make_style(**overrides):
    defaults = {
        "name": "Knotless Braids",
        "slug": "knotless-braids",
        "category": Style.Category.KNOTLESS_BRAIDS,
        "description": "A protective style using pre-stretched hair.",
        "prep_required": "Wash and detangle hair the night before.",
        "estimated_duration_minutes": 240,
        "maintenance_guidelines": "Moisturize scalp every 2-3 days.",
        "starting_price": "150.00",
    }
    defaults.update(overrides)
    return Style.objects.create(**defaults)


class StyleModelTests(TestCase):
    def test_string_representation_is_style_name(self):
        style = make_style()
        self.assertEqual(str(style), "Knotless Braids")

    def test_slug_must_be_unique(self):
        make_style()
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                make_style(name="Duplicate Slug Style")


class ReviewModelTests(TestCase):
    def test_is_approved_defaults_to_false(self):
        style = make_style()
        review = Review.objects.create(client_name="Jane Doe", rating=5, comment="Great work!", style=style)
        self.assertFalse(review.is_approved)

    def test_rating_above_five_is_invalid(self):
        style = make_style()
        review = Review(client_name="Jane Doe", rating=6, comment="Too high", style=style)
        with self.assertRaises(ValidationError):
            review.full_clean()

    def test_rating_below_one_is_invalid(self):
        style = make_style()
        review = Review(client_name="Jane Doe", rating=0, comment="Too low", style=style)
        with self.assertRaises(ValidationError):
            review.full_clean()


class BookingModelTests(TestCase):
    def test_status_defaults_to_pending(self):
        style = make_style()
        booking = Booking.objects.create(
            client_name="Jane Doe",
            client_email="jane@example.com",
            style=style,
            requested_datetime="2026-09-01T10:00:00Z",
        )
        self.assertEqual(booking.status, Booking.Status.PENDING)

    def test_deleting_style_with_bookings_is_protected(self):
        style = make_style()
        Booking.objects.create(
            client_name="Jane Doe",
            client_email="jane@example.com",
            style=style,
            requested_datetime="2026-09-01T10:00:00Z",
        )
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                style.delete()

class GalleryImageModelTests(TestCase):
    def test_string_representation_falls_back_when_no_caption(self):
        image = GalleryImage.objects.create(caption="")
        self.assertEqual(str(image), f"Gallery photo #{image.pk}")

    def test_deleting_style_sets_gallery_image_style_to_null(self):
        style = make_style()
        image = GalleryImage.objects.create(caption="Test photo", style=style)
        style.delete()
        image.refresh_from_db()
        self.assertIsNone(image.style)