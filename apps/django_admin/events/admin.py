from django.contrib import admin, messages
from django.db import models
from django.utils import timezone
from django.utils.html import format_html

from .models import Event, Order, Organizer, Ticket, TicketTier, Venue


admin.site.site_header = "Let's Go Event Operations"
admin.site.site_title = "Let's Go Admin"
admin.site.index_title = "Event catalogue and publishing"


@admin.register(Organizer)
class OrganizerAdmin(admin.ModelAdmin):
    list_display = ("name", "verified", "event_count", "updated_at")
    list_filter = ("verified",)
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}

    @admin.display(description="Events")
    def event_count(self, organizer: Organizer) -> int:
        return organizer.events.count()


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ("name", "area", "city", "county", "country", "coordinates", "coordinates_are_approximate")
    list_filter = ("county", "city", "country", "coordinates_are_approximate")
    search_fields = ("name", "address", "area", "city", "county")
    prepopulated_fields = {"slug": ("name",)}

    @admin.display(description="Coordinates")
    def coordinates(self, venue: Venue) -> str:
        return f"{venue.latitude}, {venue.longitude}"


class TicketTierInline(admin.StackedInline):
    model = TicketTier
    extra = 1
    min_num = 1
    validate_min = True
    fields = (
        "name",
        "description",
        "price_minor",
        "currency",
        "capacity",
        "sales_start_at",
        "sales_end_at",
    )


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "status_badge",
        "category",
        "venue",
        "starts_at",
        "starting_price",
        "featured",
        "hot_rank",
    )
    list_filter = ("status", "category", "featured", "hot_rank", "selling_fast", "venue__county", "venue__city")
    search_fields = ("title", "summary", "description", "venue__name", "organizer__name")
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("organizer", "venue")
    date_hierarchy = "starts_at"
    readonly_fields = ("published_at", "created_at", "updated_at")
    actions = ("publish_events", "return_to_draft")
    inlines = (TicketTierInline,)
    fieldsets = (
        ("Experience", {"fields": ("title", "slug", "summary", "description", "category", "mood")}),
        ("Organizer and venue", {"fields": ("organizer", "venue")}),
        ("Schedule", {"fields": ("starts_at", "ends_at", "timezone", "date_confirmed", "time_confirmed")}),
        ("Artwork", {"fields": ("cover_image", "external_image_url")}),
        ("Publishing", {"fields": ("status", "featured", "hot_rank", "selling_fast", "published_at")}),
        ("Guest information", {"fields": ("age_restriction", "accessibility_notes", "policies"), "classes": ("collapse",)}),
        ("System", {"fields": ("currency", "created_at", "updated_at"), "classes": ("collapse",)}),
    )

    @admin.display(description="Status")
    def status_badge(self, event: Event) -> str:
        colours = {"PUBLISHED": "#16a34a", "DRAFT": "#6b7280", "CANCELLED": "#dc2626", "POSTPONED": "#d97706"}
        return format_html(
            '<span style="background:{};color:white;padding:4px 8px;border-radius:999px;font-size:11px;font-weight:700">{}</span>',
            colours.get(event.status, "#4f46e5"),
            event.get_status_display(),
        )

    @admin.display(description="Starting price")
    def starting_price(self, event: Event) -> str:
        return f"{event.currency} {event.starting_price_minor / 100:,.0f}"

    @admin.action(description="Publish selected events")
    def publish_events(self, request, queryset) -> None:
        count = queryset.update(status=Event.Status.PUBLISHED, published_at=timezone.now())
        self.message_user(request, f"Published {count} event(s).", messages.SUCCESS)

    @admin.action(description="Return selected events to draft")
    def return_to_draft(self, request, queryset) -> None:
        count = queryset.update(status=Event.Status.DRAFT)
        self.message_user(request, f"Returned {count} event(s) to draft.", messages.WARNING)


@admin.register(TicketTier)
class TicketTierAdmin(admin.ModelAdmin):
    list_display = ("name", "event", "display_price", "capacity", "remaining_count")
    list_filter = ("currency", "event__status")
    search_fields = ("name", "event__title")
    autocomplete_fields = ("event",)

    @admin.display(description="Price")
    def display_price(self, tier: TicketTier) -> str:
        return f"{tier.currency} {tier.price_minor / 100:,.0f}"

    @admin.display(description="Remaining")
    def remaining_count(self, tier: TicketTier) -> int:
        return tier.remaining


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("reference", "event", "status", "total", "reservation_expires_at", "created_at")
    list_filter = ("status", "currency")
    search_fields = ("reference", "event__title")
    readonly_fields = ("reference", "total_minor", "currency", "reservation_expires_at", "created_at", "updated_at")
    actions = ("mark_paid_and_issue_tickets",)

    @admin.display(description="Total")
    def total(self, order: Order) -> str:
        return f"{order.currency} {order.total_minor / 100:,.0f}"

    @admin.action(description="Mark paid and issue tickets")
    def mark_paid_and_issue_tickets(self, request, queryset) -> None:
        issued = 0
        for order in queryset.filter(status=Order.Status.RESERVED).prefetch_related("items__tier"):
            for item in order.items.all():
                TicketTier.objects.filter(pk=item.tier_id).update(
                    reserved_count=models.F("reserved_count") - item.quantity,
                    sold_count=models.F("sold_count") + item.quantity,
                )
                Ticket.objects.bulk_create([Ticket(order=order, tier=item.tier) for _ in range(item.quantity)])
                issued += item.quantity
            order.status = Order.Status.PAID
            order.save(update_fields=["status", "updated_at"])
        self.message_user(request, f"Issued {issued} ticket(s).", messages.SUCCESS)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("code", "event", "tier", "order", "checked_in_at", "created_at")
    search_fields = ("code", "order__reference", "order__event__title")
    readonly_fields = ("code", "order", "tier", "checked_in_at", "created_at")

    @admin.display(description="Event")
    def event(self, ticket: Ticket) -> str:
        return ticket.order.event.title
