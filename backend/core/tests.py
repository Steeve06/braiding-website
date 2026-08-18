from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase 
from core.models import Booking, GalleryImage, Review, Style

class StyleApiTests(APITestCase):
    def test_list_only_returns_active_styles(self):
        make_style(slug="active-style", is_active=True)
        make_style(slug="inactive-style", name="Hidden Style", is_active=False)

        response = self.client.get(reverse("style-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["slug"], "active-style")

    def test_category_filter_narrows_results(self):
        make_style(slug="knotless-style", category=Style.Category.KNOTLESS_BRAIDS)
        make_style(slug="cornrow-style", name="Cornrows", category=Style.Category.CORNROWS)

        response = self.client.get(reverse("style-list"), {"category": Style.Category.CORNROWS})

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["slug"], "cornrow-style")


class ReviewApiTests(APITestCase):
    def test_list_only_returns_approved_reviews(self):
        style = make_style()
        Review.objects.create(client_name="Approved", rating=5, comment="Great", style=style, is_approved=True)
        Review.objects.create(client_name="Pending", rating=3, comment="Ok", style=style, is_approved=False)

        response = self.client.get(reverse("review-list"))

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["client_name"], "Approved")

    def test_create_ignores_client_supplied_is_approved(self):
        style = make_style()
        payload = {
            "client_name": "New Client",
            "rating": 5,
            "comment": "Sneaky attempt",
            "style": style.id,
            "is_approved": True,
        }

        response = self.client.post(reverse("review-list"), payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertFalse(response.data["is_approved"])


class BookingApiTests(APITestCase):
    def test_create_booking_succeeds(self):
        style = make_style()
        payload = {
            "client_name": "Jane Doe",
            "client_email": "jane@example.com",
            "style": style.id,
            "requested_datetime": "2026-10-01T10:00:00Z",
        }

        response = self.client.post(reverse("booking-list"), payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], Booking.Status.PENDING)

    def test_overlapping_booking_is_rejected(self):
        style = make_style()
        Booking.objects.create(
            client_name="Existing Client",
            client_email="existing@example.com",
            style=style,
            requested_datetime="2026-10-01T10:00:00Z",
        )
        payload = {
            "client_name": "Jane Doe",
            "client_email": "jane@example.com",
            "style": style.id,
            "requested_datetime": "2026-10-01T10:00:00Z",
        }

        response = self.client.post(reverse("booking-list"), payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)
        
        
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


class StyleModelTests(APITestCase):
    def test_string_representation_is_style_name(self):
        style = make_style()
        self.assertEqual(str(style), "Knotless Braids")

    def test_slug_must_be_unique(self):
        make_style()
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                make_style(name="Duplicate Slug Style")


class ReviewModelTests(APITestCase):
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


class BookingModelTests(APITestCase):
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

class GalleryImageModelTests(APITestCase):
    def test_string_representation_falls_back_when_no_caption(self):
        image = GalleryImage.objects.create(caption="")
        self.assertEqual(str(image), f"Gallery photo #{image.pk}")

    def test_deleting_style_sets_gallery_image_style_to_null(self):
        style = make_style()
        image = GalleryImage.objects.create(caption="Test photo", style=style)
        style.delete()
        image.refresh_from_db()
        self.assertIsNone(image.style)