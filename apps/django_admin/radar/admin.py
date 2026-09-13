from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.db.models import Count
from django.utils.html import format_html

from radar.models import CountyCoverage, DuplicateCandidate, EventSource, ScrapeRun, ScrapedEventObservation
from radar.security import validate_public_url
from radar.services.pipeline import publish_observation


@admin.register(EventSource)
class EventSourceAdmin(admin.ModelAdmin):
    list_display = (
        "name", "source_type", "enabled", "compliance_status", "health_badge",
        "trust_level", "last_successful_run_at",
    )
    list_filter = ("enabled", "source_type", "compliance_status", "content_usage_mode", "health_status")
    search_fields = ("name", "base_url", "adapter_name")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("last_successful_run_at", "last_failed_run_at", "failure_count", "created_at", "updated_at")
    actions = ("enable_compliant_sources", "disable_sources")

    def save_model(self, request, obj, form, change):
        obj.base_url = validate_public_url(obj.base_url)
        if obj.enabled and obj.compliance_status not in {
            EventSource.ComplianceStatus.APPROVED,
            EventSource.ComplianceStatus.APPROVED_METADATA_ONLY,
            EventSource.ComplianceStatus.PARTNER,
        }:
            raise ValidationError("A source must pass compliance review before it can be enabled.")
        super().save_model(request, obj, form, change)

    @admin.display(description="Health")
    def health_badge(self, source):
        colours = {"HEALTHY": "#16a34a", "DEGRADED": "#d97706", "FAILED": "#dc2626", "BLOCKED": "#7c3aed"}
        return format_html(
            '<span style="color:{};font-weight:700">{}</span>',
            colours.get(source.health_status, "#6b7280"), source.get_health_status_display(),
        )

    @admin.action(description="Enable selected compliance-approved sources")
    def enable_compliant_sources(self, request, queryset):
        approved = queryset.filter(compliance_status__in=["APPROVED", "APPROVED_METADATA_ONLY", "PARTNER"])
        count = approved.update(enabled=True)
        self.message_user(request, f"Enabled {count} approved source(s).", messages.SUCCESS)

    @admin.action(description="Disable selected sources")
    def disable_sources(self, request, queryset):
        count = queryset.update(enabled=False)
        self.message_user(request, f"Disabled {count} source(s).", messages.WARNING)


@admin.register(ScrapeRun)
class ScrapeRunAdmin(admin.ModelAdmin):
    list_display = ("source", "status", "created_at", "observations_created", "pages_succeeded", "correlation_id")
    list_filter = ("status", "source")
    search_fields = ("source__name", "correlation_id", "safe_error_message")
    readonly_fields = [field.name for field in ScrapeRun._meta.fields]

    def has_add_permission(self, request):
        return False


class DuplicateInline(admin.TabularInline):
    model = DuplicateCandidate
    extra = 0
    readonly_fields = ("candidate_event", "score", "reasons", "status", "created_at")
    can_delete = False


@admin.register(ScrapedEventObservation)
class ObservationAdmin(admin.ModelAdmin):
    list_display = ("normalized_title", "source", "start_at", "city", "county", "quality_badge", "review_status")
    list_filter = ("review_status", "source", "county", "category", "is_free")
    search_fields = ("raw_title", "normalized_title", "venue_name", "city", "organizer_name", "source_url")
    readonly_fields = ("fingerprint", "quality_score", "validation_issues", "canonical_event", "created_at", "updated_at")
    actions = ("approve_observations", "publish_observations", "reject_observations")
    inlines = (DuplicateInline,)
    date_hierarchy = "start_at"

    @admin.display(description="Quality")
    def quality_badge(self, observation):
        colour = "#16a34a" if observation.quality_score >= 80 else "#d97706" if observation.quality_score >= 60 else "#dc2626"
        return format_html('<strong style="color:{}">{}/100</strong>', colour, observation.quality_score)

    @admin.action(description="Approve selected observations")
    def approve_observations(self, request, queryset):
        count = queryset.filter(quality_score__gte=60).update(review_status="APPROVED")
        self.message_user(request, f"Approved {count} observation(s).", messages.SUCCESS)

    @admin.action(description="Publish selected observations to the event catalogue")
    def publish_observations(self, request, queryset):
        published = 0
        failed = 0
        for observation in queryset.select_related("source"):
            try:
                publish_observation(observation)
                published += 1
            except ValueError:
                failed += 1
        self.message_user(request, f"Published {published}; skipped {failed} invalid observation(s).", messages.SUCCESS if not failed else messages.WARNING)

    @admin.action(description="Reject selected observations")
    def reject_observations(self, request, queryset):
        count = queryset.update(review_status="REJECTED")
        self.message_user(request, f"Rejected {count} observation(s).", messages.WARNING)


@admin.register(DuplicateCandidate)
class DuplicateCandidateAdmin(admin.ModelAdmin):
    list_display = ("observation", "candidate_event", "score", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("observation__normalized_title", "candidate_event__title")


@admin.register(CountyCoverage)
class CountyCoverageAdmin(admin.ModelAdmin):
    list_display = ("county", "known_upcoming_events", "active_sources", "last_discovery_at", "has_gap")
    search_fields = ("county", "gap_recommendation")
    readonly_fields = ("county", "known_upcoming_events", "active_sources", "categories_represented", "last_discovery_at", "gap_recommendation", "updated_at")
    ordering = ("-known_upcoming_events", "county")

    @admin.display(boolean=True, description="Radar gap")
    def has_gap(self, coverage):
        return bool(coverage.gap_recommendation)

    def has_add_permission(self, request):
        return False
