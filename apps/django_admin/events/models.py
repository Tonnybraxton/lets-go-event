import uuid
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class Organizer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    description = models.TextField(blank=True)
    verified = models.BooleanField(default=False)
    website_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Venue(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=140)
    slug = models.SlugField(max_length=160, unique=True)
    address = models.CharField(max_length=220)
    area = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100)
    county = models.CharField(max_length=100, blank=True, db_index=True)
    country = models.CharField(max_length=100, default="Kenya")
    country_code = models.CharField(max_length=2, default="KE")
    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        validators=[MinValueValidator(Decimal("-90")), MaxValueValidator(Decimal("90"))],
    )
    longitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        validators=[MinValueValidator(Decimal("-180")), MaxValueValidator(Decimal("180"))],
    )
    timezone = models.CharField(max_length=80, default="Africa/Nairobi")
    coordinates_are_approximate = models.BooleanField(
        default=False,
        help_text="Mark this when the source only identifies a town or county rather than an exact venue pin.",
    )
    accessibility_notes = models.TextField(blank=True)
    parking_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["city", "name"]
        indexes = [models.Index(fields=["city"])]

    def __str__(self) -> str:
        return f"{self.name} — {self.city}"


class Event(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        PUBLISHED = "PUBLISHED", "Published"
        POSTPONED = "POSTPONED", "Postponed"
        CANCELLED = "CANCELLED", "Cancelled"
        COMPLETED = "COMPLETED", "Completed"

    CATEGORIES = [
        ("Music", "Music"),
        ("Nightlife", "Nightlife"),
        ("Festivals", "Festivals"),
        ("Comedy", "Comedy"),
        ("Sports", "Sports"),
        ("Conferences", "Conferences"),
        ("Family", "Family"),
        ("Food & Drink", "Food & Drink"),
        ("Experiences", "Experiences"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organizer = models.ForeignKey(Organizer, on_delete=models.PROTECT, related_name="events")
    venue = models.ForeignKey(Venue, on_delete=models.PROTECT, related_name="events")
    title = models.CharField(max_length=140)
    slug = models.SlugField(max_length=160, unique=True)
    summary = models.CharField(max_length=240)
    description = models.TextField()
    category = models.CharField(max_length=60, choices=CATEGORIES)
    mood = models.CharField(max_length=80, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    timezone = models.CharField(max_length=80, default="Africa/Nairobi")
    currency = models.CharField(max_length=3, default="KES")
    cover_image = models.ImageField(upload_to="events/%Y/%m/", blank=True)
    external_image_url = models.URLField(
        blank=True,
        help_text="Optional fallback when no cover image is uploaded.",
    )
    selling_fast = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    hot_rank = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        unique=True,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Optional position in the curated Top 10 upcoming Kenya collection.",
    )
    date_confirmed = models.BooleanField(
        default=True,
        help_text="Clear this when a date is corroborated externally but still needs organizer confirmation.",
    )
    time_confirmed = models.BooleanField(
        default=True,
        help_text="Clear this when the source confirms the date but has not published a start time.",
    )
    age_restriction = models.CharField(max_length=40, blank=True)
    accessibility_notes = models.TextField(blank=True)
    policies = models.TextField(blank=True)
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["starts_at"]
        indexes = [
            models.Index(fields=["status", "starts_at"]),
            models.Index(fields=["category", "starts_at"]),
        ]

    def clean(self) -> None:
        super().clean()
        if self.starts_at and self.ends_at and self.ends_at <= self.starts_at:
            raise ValidationError({"ends_at": "The event must end after it starts."})
        if not self.cover_image and not self.external_image_url:
            raise ValidationError(
                {"external_image_url": "Upload a cover image or provide an external image URL."}
            )

    def save(self, *args, **kwargs) -> None:
        if self.status == self.Status.PUBLISHED and self.published_at is None:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    @property
    def starting_price_minor(self) -> int:
        amount = self.ticket_tiers.aggregate(models.Min("price_minor"))["price_minor__min"]
        return amount or 0

    def __str__(self) -> str:
        return self.title


class TicketTier(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="ticket_tiers")
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=180, blank=True)
    price_minor = models.PositiveBigIntegerField(
        help_text="Price in minor units. Example: KES 1,500 is entered as 150000."
    )
    currency = models.CharField(max_length=3, default="KES")
    capacity = models.PositiveIntegerField()
    sold_count = models.PositiveIntegerField(default=0, editable=False)
    reserved_count = models.PositiveIntegerField(default=0, editable=False)
    sales_start_at = models.DateTimeField(blank=True, null=True)
    sales_end_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["price_minor", "name"]
        constraints = [
            models.UniqueConstraint(fields=["event", "name"], name="unique_event_ticket_tier")
        ]

    @property
    def remaining(self) -> int:
        return max(0, self.capacity - self.sold_count - self.reserved_count)

    def clean(self) -> None:
        super().clean()
        if self.sold_count + self.reserved_count > self.capacity:
            raise ValidationError("Sold and reserved tickets cannot exceed capacity.")
        if self.sales_start_at and self.sales_end_at and self.sales_end_at <= self.sales_start_at:
            raise ValidationError({"sales_end_at": "Ticket sales must end after they start."})

    def __str__(self) -> str:
        return f"{self.event.title} — {self.name}"


class Order(models.Model):
    """A short-lived ticket reservation that a payment provider can settle later."""

    class Status(models.TextChoices):
        RESERVED = "RESERVED", "Reserved"
        PAID = "PAID", "Paid"
        EXPIRED = "EXPIRED", "Expired"
        CANCELLED = "CANCELLED", "Cancelled"

    class PaymentStatus(models.TextChoices):
        NOT_STARTED = "NOT_STARTED", "Not started"
        PENDING = "PENDING", "Pending"
        COMPLETED = "COMPLETED", "Completed"
        FAILED = "FAILED", "Failed"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reference = models.CharField(max_length=32, unique=True, editable=False)
    event = models.ForeignKey(Event, on_delete=models.PROTECT, related_name="orders")
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.RESERVED)
    total_minor = models.PositiveBigIntegerField()
    currency = models.CharField(max_length=3, default="KES")
    reservation_expires_at = models.DateTimeField()
    phone_number = models.CharField(max_length=12, blank=True)
    payment_status = models.CharField(max_length=16, choices=PaymentStatus.choices, default=PaymentStatus.NOT_STARTED)
    checkout_request_id = models.CharField(max_length=100, blank=True, null=True, unique=True)
    merchant_request_id = models.CharField(max_length=100, blank=True)
    mpesa_receipt_number = models.CharField(max_length=32, blank=True)
    payment_result_desc = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs) -> None:
        if not self.reference:
            self.reference = f"LGE-{uuid.uuid4().hex[:10].upper()}"
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.reference


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    tier = models.ForeignKey(TicketTier, on_delete=models.PROTECT, related_name="order_items")
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(6)])
    unit_price_minor = models.PositiveBigIntegerField()

    class Meta:
        constraints = [models.UniqueConstraint(fields=["order", "tier"], name="unique_order_tier")]


class Ticket(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=32, unique=True, editable=False)
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name="tickets")
    tier = models.ForeignKey(TicketTier, on_delete=models.PROTECT, related_name="issued_tickets")
    checked_in_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def save(self, *args, **kwargs) -> None:
        if not self.code:
            self.code = f"LGE-{uuid.uuid4().hex[:12].upper()}"
        super().save(*args, **kwargs)


class LocationSuggestion(models.Model):
    county = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    event_type = models.CharField(max_length=100)
    timing = models.CharField(max_length=50)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "location suggestion"
        verbose_name_plural = "location suggestions"

    def __str__(self) -> str:
        return f"{self.area}, {self.county} — {self.event_type}"

