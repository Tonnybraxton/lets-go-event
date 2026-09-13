import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class EventSource(models.Model):
    class SourceType(models.TextChoices):
        PARTNER_API = "PARTNER_API", "Partner API"
        PUBLIC_API = "PUBLIC_API", "Public API"
        RSS = "RSS", "RSS"
        ICS = "ICS", "ICS / iCalendar"
        JSON_LD = "JSON_LD", "JSON-LD"
        SITEMAP = "SITEMAP", "Sitemap"
        STATIC_HTML = "STATIC_HTML", "Static HTML"
        PLAYWRIGHT = "PLAYWRIGHT", "Playwright"
        MANUAL = "MANUAL", "Manual"
        OTHER = "OTHER", "Other"

    class ComplianceStatus(models.TextChoices):
        NOT_REVIEWED = "NOT_REVIEWED", "Not reviewed"
        APPROVED = "APPROVED", "Approved"
        APPROVED_METADATA_ONLY = "APPROVED_METADATA_ONLY", "Approved metadata only"
        PARTNER = "PARTNER", "Partner"
        REQUIRES_PERMISSION = "REQUIRES_PERMISSION", "Requires permission"
        BLOCKED = "BLOCKED", "Blocked"
        DISABLED = "DISABLED", "Disabled"

    class UsageMode(models.TextChoices):
        FULL_PARTNER_CONTENT = "FULL_PARTNER_CONTENT", "Full partner content"
        PUBLIC_METADATA = "PUBLIC_METADATA", "Public metadata"
        METADATA_ONLY = "METADATA_ONLY", "Metadata only"
        SOURCE_LINK_ONLY = "SOURCE_LINK_ONLY", "Source link only"
        DISABLED_PENDING_REVIEW = "DISABLED_PENDING_REVIEW", "Disabled pending review"

    class HealthStatus(models.TextChoices):
        UNKNOWN = "UNKNOWN", "Unknown"
        HEALTHY = "HEALTHY", "Healthy"
        DEGRADED = "DEGRADED", "Degraded"
        FAILED = "FAILED", "Failed"
        BLOCKED = "BLOCKED", "Blocked"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, unique=True)
    base_url = models.URLField()
    source_type = models.CharField(max_length=24, choices=SourceType.choices)
    adapter_name = models.CharField(max_length=120, default="generic_jsonld")
    adapter_config = models.JSONField(default=dict, blank=True)
    domain_aliases = models.JSONField(default=list, blank=True)
    country = models.CharField(max_length=80, default="Kenya")
    enabled = models.BooleanField(default=False)
    priority = models.PositiveSmallIntegerField(default=50)
    trust_level = models.PositiveSmallIntegerField(
        default=30, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    default_category = models.CharField(max_length=60, blank=True)
    crawl_frequency_minutes = models.PositiveIntegerField(default=1440)
    max_concurrent_requests = models.PositiveSmallIntegerField(default=2)
    download_delay_seconds = models.DecimalField(max_digits=5, decimal_places=2, default=2)
    requires_javascript = models.BooleanField(default=False)
    requires_review = models.BooleanField(default=True)
    auto_publish_allowed = models.BooleanField(default=False)
    robots_policy = models.TextField(blank=True)
    compliance_status = models.CharField(
        max_length=32, choices=ComplianceStatus.choices, default=ComplianceStatus.NOT_REVIEWED
    )
    content_usage_mode = models.CharField(
        max_length=32,
        choices=UsageMode.choices,
        default=UsageMode.DISABLED_PENDING_REVIEW,
    )
    last_compliance_review_at = models.DateTimeField(blank=True, null=True)
    last_successful_run_at = models.DateTimeField(blank=True, null=True)
    last_failed_run_at = models.DateTimeField(blank=True, null=True)
    failure_count = models.PositiveIntegerField(default=0)
    health_status = models.CharField(
        max_length=16, choices=HealthStatus.choices, default=HealthStatus.UNKNOWN
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["priority", "name"]

    @property
    def may_crawl(self) -> bool:
        return self.enabled and self.compliance_status in {
            self.ComplianceStatus.APPROVED,
            self.ComplianceStatus.APPROVED_METADATA_ONLY,
            self.ComplianceStatus.PARTNER,
        }

    def __str__(self) -> str:
        return self.name


class ScrapeRun(models.Model):
    class Status(models.TextChoices):
        QUEUED = "QUEUED", "Queued"
        RUNNING = "RUNNING", "Running"
        SUCCEEDED = "SUCCEEDED", "Succeeded"
        PARTIAL = "PARTIAL", "Partial"
        FAILED = "FAILED", "Failed"
        BLOCKED = "BLOCKED", "Blocked"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    source = models.ForeignKey(EventSource, on_delete=models.PROTECT, related_name="runs")
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.QUEUED)
    started_at = models.DateTimeField(blank=True, null=True)
    finished_at = models.DateTimeField(blank=True, null=True)
    pages_requested = models.PositiveIntegerField(default=0)
    pages_succeeded = models.PositiveIntegerField(default=0)
    observations_created = models.PositiveIntegerField(default=0)
    safe_error_message = models.TextField(blank=True)
    correlation_id = models.UUIDField(default=uuid.uuid4, editable=False)
    metrics = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.source.name} - {self.created_at:%Y-%m-%d %H:%M}"


class ScrapedEventObservation(models.Model):
    class ReviewStatus(models.TextChoices):
        NEW = "NEW", "New"
        NORMALIZED = "NORMALIZED", "Normalized"
        NEEDS_REVIEW = "NEEDS_REVIEW", "Needs review"
        APPROVED = "APPROVED", "Approved"
        PUBLISHED = "PUBLISHED", "Published"
        REJECTED = "REJECTED", "Rejected"
        DUPLICATE = "DUPLICATE", "Duplicate"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    source = models.ForeignKey(EventSource, on_delete=models.PROTECT, related_name="observations")
    run = models.ForeignKey(
        ScrapeRun, on_delete=models.SET_NULL, related_name="observations", blank=True, null=True
    )
    source_event_id = models.CharField(max_length=240, blank=True)
    source_url = models.URLField(max_length=1000)
    canonical_source_url = models.URLField(max_length=1000, blank=True)
    raw_title = models.CharField(max_length=300)
    normalized_title = models.CharField(max_length=300, blank=True)
    raw_description = models.TextField(blank=True)
    clean_description = models.TextField(blank=True)
    raw_start = models.CharField(max_length=200, blank=True)
    raw_end = models.CharField(max_length=200, blank=True)
    start_at = models.DateTimeField(blank=True, null=True)
    end_at = models.DateTimeField(blank=True, null=True)
    timezone = models.CharField(max_length=80, default="Africa/Nairobi")
    raw_venue = models.CharField(max_length=240, blank=True)
    venue_name = models.CharField(max_length=240, blank=True)
    raw_address = models.CharField(max_length=300, blank=True)
    address = models.CharField(max_length=300, blank=True)
    city = models.CharField(max_length=100, blank=True)
    county = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, default="Kenya")
    latitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    raw_category = models.CharField(max_length=120, blank=True)
    category = models.CharField(max_length=60, blank=True)
    raw_price = models.CharField(max_length=120, blank=True)
    price_min_minor = models.PositiveBigIntegerField(blank=True, null=True)
    price_max_minor = models.PositiveBigIntegerField(blank=True, null=True)
    currency = models.CharField(max_length=3, default="KES")
    is_free = models.BooleanField(default=False)
    organizer_name = models.CharField(max_length=180, blank=True)
    ticket_url = models.URLField(max_length=1000, blank=True)
    image_url = models.URLField(max_length=1000, blank=True)
    fingerprint = models.CharField(max_length=64, db_index=True, blank=True)
    quality_score = models.PositiveSmallIntegerField(default=0)
    review_status = models.CharField(
        max_length=20, choices=ReviewStatus.choices, default=ReviewStatus.NEW
    )
    validation_issues = models.JSONField(default=list, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    canonical_event = models.ForeignKey(
        "events.Event", on_delete=models.SET_NULL, blank=True, null=True, related_name="radar_observations"
    )
    retrieved_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["source", "source_url"], name="unique_radar_source_event_url"
            )
        ]
        indexes = [
            models.Index(fields=["review_status", "quality_score"]),
            models.Index(fields=["county", "start_at"]),
        ]

    def __str__(self) -> str:
        return self.normalized_title or self.raw_title


class DuplicateCandidate(models.Model):
    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        CONFIRMED = "CONFIRMED", "Confirmed duplicate"
        DISMISSED = "DISMISSED", "Not a duplicate"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    observation = models.ForeignKey(
        ScrapedEventObservation, on_delete=models.CASCADE, related_name="duplicate_candidates"
    )
    candidate_event = models.ForeignKey(
        "events.Event", on_delete=models.CASCADE, related_name="radar_duplicate_candidates"
    )
    score = models.DecimalField(max_digits=5, decimal_places=2)
    reasons = models.JSONField(default=list)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.OPEN)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-score"]
        constraints = [
            models.UniqueConstraint(
                fields=["observation", "candidate_event"], name="unique_radar_duplicate_candidate"
            )
        ]


class CountyCoverage(models.Model):
    county = models.CharField(max_length=100, unique=True)
    known_upcoming_events = models.PositiveIntegerField(default=0)
    active_sources = models.PositiveIntegerField(default=0)
    categories_represented = models.JSONField(default=list)
    last_discovery_at = models.DateTimeField(blank=True, null=True)
    gap_recommendation = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["county"]

    def __str__(self) -> str:
        return self.county
