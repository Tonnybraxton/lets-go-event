from datetime import datetime
from decimal import Decimal
from io import BytesIO
from zoneinfo import ZoneInfo

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from PIL import Image, ImageDraw, ImageFont

from events.models import Event, Organizer, TicketTier, Venue
from radar.models import EventSource, ScrapedEventObservation
from radar.services.pipeline import build_fingerprint, quality_score


TICKETSASA_URL = "https://www.ticketsasa.com/events/fally-ipupa-live-in-nairobi"
CORROBORATING_URL = "https://ticketyetu.com/event/fally-ipupa-live-in-nairobi-349/register"
NEWS_URL = (
    "https://k24.digital/entertainment/celebrity/"
    "fally-ipupa-confirms-kenyan-show-in-september-2026/amp"
)
MAP_URL = "https://www.openstreetmap.org/way/40006019"


def _placeholder_cover() -> ContentFile:
    """Create an unmistakable temporary cover until editorial artwork is uploaded."""
    width, height = 1600, 900
    image = Image.new("RGB", (width, height), "#10091d")
    draw = ImageDraw.Draw(image)

    for y in range(height):
        progress = y / height
        colour = (
            round(18 + 37 * progress),
            round(10 + 6 * progress),
            round(34 + 46 * progress),
        )
        draw.line((0, y, width, y), fill=colour)

    draw.ellipse((1080, -270, 1750, 400), fill="#6d28d9")
    draw.ellipse((-300, 580, 350, 1230), fill="#f97316")
    draw.rounded_rectangle(
        (96, 90, 1504, 810),
        radius=36,
        outline="#c4b5fd",
        width=3,
    )

    try:
        title_font = ImageFont.load_default(size=96)
        subtitle_font = ImageFont.load_default(size=42)
        detail_font = ImageFont.load_default(size=30)
    except TypeError:  # Pillow fallback for environments without scalable default fonts.
        title_font = subtitle_font = detail_font = ImageFont.load_default()

    draw.text((150, 190), "FALLY IPUPA", font=title_font, fill="#ffffff")
    draw.text((155, 315), "LIVE IN NAIROBI", font=subtitle_font, fill="#ddd6fe")
    draw.text(
        (155, 510),
        "SAT 05 SEP 2026  -  UHURU GARDENS",
        font=detail_font,
        fill="#ffffff",
    )
    draw.text(
        (155, 690),
        "TEMPORARY COVER  -  REPLACE IN DJANGO ADMIN",
        font=detail_font,
        fill="#fed7aa",
    )

    output = BytesIO()
    image.save(output, format="PNG", optimize=True)
    return ContentFile(output.getvalue())


class Command(BaseCommand):
    help = "Create or update the curated Fally Ipupa TicketSasa listing"

    @transaction.atomic
    def handle(self, *args, **options):
        nairobi = ZoneInfo("Africa/Nairobi")
        starts_at = datetime(2026, 9, 5, 15, 0, tzinfo=nairobi)
        ends_at = datetime(2026, 9, 6, 3, 0, tzinfo=nairobi)
        sales_end_at = datetime(2026, 8, 31, 23, 59, tzinfo=nairobi)

        source, _ = EventSource.objects.get_or_create(
            slug="ticketsasa",
            defaults={
                "name": "TicketSasa",
                "base_url": "https://www.ticketsasa.com/",
                "source_type": EventSource.SourceType.MANUAL,
                "adapter_name": "manual_editorial",
                "enabled": False,
                "requires_review": True,
                "auto_publish_allowed": False,
                "compliance_status": EventSource.ComplianceStatus.NOT_REVIEWED,
                "content_usage_mode": EventSource.UsageMode.SOURCE_LINK_ONLY,
            },
        )

        organizer, _ = Organizer.objects.update_or_create(
            slug="ticket-yetu-radio-africa",
            defaults={
                "name": "Ticket YETU by Radio Africa",
                "description": "Host label shown on the primary TicketSasa listing.",
                "verified": False,
            },
        )
        venue, _ = Venue.objects.update_or_create(
            slug="uhuru-gardens-nairobi",
            defaults={
                "name": "Uhuru Gardens",
                "address": "Lang'ata Road",
                "area": "Lang'ata",
                "city": "Nairobi",
                "country": "Kenya",
                "country_code": "KE",
                "latitude": Decimal("-1.3259300"),
                "longitude": Decimal("36.7993000"),
                "timezone": "Africa/Nairobi",
                "parking_notes": "Confirm parking and event-day access with the ticket source.",
            },
        )

        summary = (
            "Congolese superstar Fally Ipupa brings rumba, soukous and Afropop "
            "to Uhuru Gardens for a major Nairobi concert."
        )
        description = (
            "Fally Ipupa headlines a twelve-hour Nairobi show at Uhuru Gardens. "
            "A corroborating event listing advertises Kamo Mphela, Tango Supreme, "
            "DJ Maphorisa, DJ Ice, Joe Mfalme and Kodong Klan on the supporting bill. "
            "Lineup, availability and entry policies can change, so confirm the latest "
            "details on TicketSasa before booking."
        )

        event = Event.objects.filter(slug="fally-ipupa-live-in-nairobi").first()
        created = event is None
        if event is None:
            event = Event(slug="fally-ipupa-live-in-nairobi")

        event.organizer = organizer
        event.venue = venue
        event.title = "Fally Ipupa Live in Nairobi"
        event.summary = summary
        event.description = description
        event.category = "Music"
        event.mood = "Dance all night"
        event.status = Event.Status.PUBLISHED
        event.starts_at = starts_at
        event.ends_at = ends_at
        event.timezone = "Africa/Nairobi"
        event.currency = "KES"
        event.featured = False
        event.selling_fast = False
        event.policies = (
            "External checkout is managed by TicketSasa. Current Wave 1 prices were "
            "checked on 13 August 2026 and may change. Listed sales close 31 August 2026 "
            "at 11:59 PM EAT; confirm availability and final terms at the source. "
            f"Source: {TICKETSASA_URL}"
        )

        if not event.cover_image and not event.external_image_url:
            event.cover_image.save(
                "fally-ipupa-cover-pending.png",
                _placeholder_cover(),
                save=False,
            )

        event.full_clean()
        event.save()

        tiers = (
            ("Wave 1 Regular", 1_000_000),
            ("Wave 1 VIP", 3_000_000),
            ("Wave 1 VVIP", 4_000_000),
        )
        for name, price_minor in tiers:
            tier, _ = TicketTier.objects.update_or_create(
                event=event,
                name=name,
                defaults={
                    "description": "Current TicketSasa price; confirm live availability at the source.",
                    "price_minor": price_minor,
                    "currency": "KES",
                    "capacity": 1,
                    "sales_end_at": sales_end_at,
                },
            )
            tier.full_clean()
            tier.save()

        observation, _ = ScrapedEventObservation.objects.update_or_create(
            source=source,
            source_url=TICKETSASA_URL,
            defaults={
                "source_event_id": "fally-ipupa-live-in-nairobi",
                "canonical_source_url": TICKETSASA_URL,
                "raw_title": "Fally Ipupa Live in Nairobi",
                "normalized_title": "Fally Ipupa Live in Nairobi",
                "raw_description": "",
                "clean_description": description,
                "raw_start": "SAT 05 SEP 2026 03:00 PM",
                "raw_end": "SUN 06 SEP 2026 03:00 AM",
                "start_at": starts_at,
                "end_at": ends_at,
                "timezone": "Africa/Nairobi",
                "raw_venue": "Uhuru Gardens, Nairobi, Kenya",
                "venue_name": "Uhuru Gardens",
                "raw_address": "Uhuru Gardens, Lang'ata Road, Nairobi, Kenya",
                "address": "Lang'ata Road",
                "city": "Nairobi",
                "county": "Nairobi",
                "country": "Kenya",
                "latitude": Decimal("-1.3259300"),
                "longitude": Decimal("36.7993000"),
                "raw_category": "Music",
                "category": "Music",
                "raw_price": "Wave 1 Regular KES 10,000; VIP KES 30,000; VVIP KES 40,000",
                "price_min_minor": 1_000_000,
                "price_max_minor": 4_000_000,
                "currency": "KES",
                "is_free": False,
                "organizer_name": "Ticket YETU - By RADIO AFRICA",
                "ticket_url": TICKETSASA_URL,
                "image_url": "",
                "fingerprint": build_fingerprint(
                    "Fally Ipupa Live in Nairobi", starts_at, "Uhuru Gardens", "Nairobi"
                ),
                "review_status": ScrapedEventObservation.ReviewStatus.PUBLISHED,
                "canonical_event": event,
                "retrieved_at": timezone.now(),
                "metadata": {
                    "ingestion": "manual_editorial",
                    "primary_source": TICKETSASA_URL,
                    "corroborating_sources": [CORROBORATING_URL, NEWS_URL],
                    "venue_map_source": MAP_URL,
                    "supporting_lineup_source": CORROBORATING_URL,
                    "organizer_note": (
                        "Seller and event-guide organizer labels conflict; the primary "
                        "TicketSasa host label is used and remains unverified."
                    ),
                    "image_status": "awaiting_editor_upload",
                },
            },
        )
        observation.quality_score, observation.validation_issues = quality_score(observation)
        observation.review_status = ScrapedEventObservation.ReviewStatus.PUBLISHED
        observation.canonical_event = event
        observation.save(
            update_fields=[
                "quality_score",
                "validation_issues",
                "review_status",
                "canonical_event",
                "updated_at",
            ]
        )

        action = "Created" if created else "Updated"
        self.stdout.write(
            self.style.SUCCESS(
                f"{action} Fally Ipupa Live in Nairobi as the featured TicketSasa listing."
            )
        )
