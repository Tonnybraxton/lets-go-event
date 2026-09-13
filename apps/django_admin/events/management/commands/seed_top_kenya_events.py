from datetime import datetime
from decimal import Decimal
from zoneinfo import ZoneInfo

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from events.curation import build_editorial_placeholder
from events.models import Event, Organizer, TicketTier, Venue
from radar.models import EventSource, ScrapedEventObservation
from radar.services.pipeline import build_fingerprint, quality_score
from radar.tasks import refresh_coverage


NAIROBI = ZoneInfo("Africa/Nairobi")


def at(year, month, day, hour=12, minute=0):
    return datetime(year, month, day, hour, minute, tzinfo=NAIROBI)


EVENTS = (
    {
        "rank": 1,
        "slug": "nyeri-colour-festival-2026",
        "title": "Nyeri Colour Festival 2026",
        "summary": "A bright day of colour, music and community at Kamukunji Ground in Nyeri.",
        "description": (
            "Nyeri Colour Festival invites guests to a daytime colour celebration at Kamukunji "
            "Ground. The ticket listing publishes early-bird, regular, gate, VIP and group options."
        ),
        "category": "Festivals",
        "mood": "Meet new people",
        "starts_at": at(2026, 8, 15, 8),
        "ends_at": at(2026, 8, 15, 18),
        "time_confirmed": True,
        "date_label": "15 Aug 2026",
        "organizer": "Nyeri Colour Festival",
        "organizer_slug": "nyeri-colour-festival",
        "venue": "Kamukunji Ground",
        "venue_slug": "kamukunji-ground-nyeri",
        "address": "Kamukunji Ground",
        "area": "Nyeri Town",
        "city": "Nyeri",
        "county": "Nyeri",
        "latitude": "-0.4201300",
        "longitude": "36.9475900",
        "approximate": True,
        "source": ("Little Events", "little-events", "https://apps.little.africa/"),
        "source_url": "https://apps.little.africa/events/208",
        "raw_price": "Early Bird KES 400; Regular KES 500; VIP KES 1,200",
        "price_min": 40_000,
        "price_max": 120_000,
        "tiers": (("Early Bird", 40_000), ("Regular", 50_000), ("VIP", 120_000)),
        "schedule_note": "The source confirms an 8:00 AM first show; final closing time should be reconfirmed.",
    },
    {
        "rank": 2,
        "slug": "the-muskats-kisii-2026",
        "title": "The Muskats",
        "summary": "A contemporary Kisii cultural gathering built around heritage, music and storytelling.",
        "description": (
            "The Muskats brings Kisii heritage into a modern festival setting through music, "
            "storytelling, fashion and locally selected DJs. The ticket source currently names "
            "Kisii County but does not publish a precise venue pin."
        ),
        "category": "Festivals",
        "mood": "Celebrate culture",
        "starts_at": at(2026, 8, 22, 11),
        "ends_at": at(2026, 8, 22, 23, 1),
        "time_confirmed": True,
        "date_label": "22 Aug 2026",
        "organizer": "The Muskats",
        "organizer_slug": "the-muskats",
        "venue": "Kisii County — venue to be confirmed",
        "venue_slug": "the-muskats-kisii-county",
        "address": "Confirm the exact venue on the ticket source",
        "area": "Kisii Town",
        "city": "Kisii",
        "county": "Kisii",
        "latitude": "-0.6817400",
        "longitude": "34.7666600",
        "approximate": True,
        "source": ("Little Events", "little-events", "https://apps.little.africa/"),
        "source_url": "https://apps.little.africa/events/the-muskats",
        "raw_price": "Kids KES 400; Regular Phase 2 KES 1,600; VIP Phase 2 KES 3,000",
        "price_min": 40_000,
        "price_max": 300_000,
        "tiers": (("Kids", 40_000), ("Regular Phase 2", 160_000), ("VIP Phase 2", 300_000)),
        "schedule_note": "The source publishes the county but not a precise venue address.",
    },
    {
        "rank": 3,
        "slug": "nakuru-colour-splash-2026",
        "title": "Nakuru Colour Splash",
        "summary": "Colour throws, DJs, dancing, games and food in a high-energy Nakuru day out.",
        "description": (
            "Nakuru Colour Splash is advertised as a daytime colour experience at NVP Garden "
            "with music, DJs, games, dancing and food. Guests are encouraged to wear white."
        ),
        "category": "Festivals",
        "mood": "Meet new people",
        "starts_at": at(2026, 8, 22, 10),
        "ends_at": at(2026, 8, 22, 18),
        "time_confirmed": True,
        "date_label": "22 Aug 2026",
        "organizer": "Street Vibe Movement",
        "organizer_slug": "street-vibe-movement",
        "venue": "NVP Garden",
        "venue_slug": "nvp-garden-nakuru",
        "address": "NVP Garden",
        "area": "Nakuru Town",
        "city": "Nakuru",
        "county": "Nakuru",
        "latitude": "-0.3324170",
        "longitude": "36.0354550",
        "approximate": True,
        "source": ("Ticketvort", "ticketvort", "https://ticketvort.com/"),
        "source_url": "https://ticketvort.com/event-ticketing/nakuru-colour-splash/",
        "raw_price": "Regular KES 500; Gate KES 800; VIP KES 1,500",
        "price_min": 50_000,
        "price_max": 150_000,
        "tiers": (("Regular", 50_000), ("Gate", 80_000), ("VIP", 150_000)),
        "schedule_note": "Ticketvort publishes 10:00 AM to 6:00 PM.",
    },
    {
        "rank": 4,
        "slug": "eldoret-food-festival-4",
        "title": "Eldoret Food Festival 4.0",
        "summary": "A day of food, culture and community at Naveen Resort in Eldoret.",
        "description": (
            "The fourth Eldoret Food Festival brings local flavours and community entertainment "
            "to Naveen Resort, Elgon View. The ticket source has published the date and prices "
            "but not a start time."
        ),
        "category": "Food & Drink",
        "mood": "Taste something new",
        "starts_at": at(2026, 8, 30, 12),
        "ends_at": at(2026, 8, 30, 20),
        "time_confirmed": False,
        "date_label": "30 Aug 2026",
        "organizer": "Eldoret Food Festival",
        "organizer_slug": "eldoret-food-festival",
        "venue": "Naveen Resort, Elgon View",
        "venue_slug": "naveen-resort-elgon-view",
        "address": "Elgon View",
        "area": "Elgon View",
        "city": "Eldoret",
        "county": "Uasin Gishu",
        "latitude": "0.5030000",
        "longitude": "35.2600000",
        "approximate": True,
        "source": ("Madfun", "madfun", "https://gigs.madfun.com/"),
        "source_url": "https://gigs.madfun.com/event/863",
        "raw_price": "Early Bird KES 599; Group of 3 KES 1,250",
        "price_min": 59_900,
        "price_max": 125_000,
        "tiers": (("Early Bird", 59_900), ("Early Bird Group of 3", 125_000)),
        "schedule_note": "The seller publishes the date only; confirm the start time before travel.",
    },
    {
        "rank": 6,
        "slug": "tenwek-heart-run-hearts-in-motion-2026",
        "title": "Tenwek Heart Run — Hearts in Motion",
        "summary": "A Bomet charity run raising support for patients who need life-saving heart surgery.",
        "description": (
            "AGC Tenwek Hospital's Hearts in Motion run supports patients who cannot afford "
            "life-saving surgery. The organizer publishes arrival, assembly, race time and "
            "registration details; the 5 September 2026 date is from the Kenyan athletics calendar "
            "and should be confirmed with the organizer before travel."
        ),
        "category": "Sports",
        "mood": "Move for a cause",
        "starts_at": at(2026, 9, 5, 5, 45),
        "ends_at": at(2026, 9, 5, 12),
        "date_confirmed": False,
        "time_confirmed": True,
        "date_label": "05 Sep 2026",
        "organizer": "AGC Tenwek Hospital",
        "organizer_slug": "agc-tenwek-hospital",
        "venue": "AGC Tenwek Hospital",
        "venue_slug": "agc-tenwek-hospital",
        "address": "Tenwek Hospital",
        "area": "Tenwek",
        "city": "Bomet",
        "county": "Bomet",
        "latitude": "-0.7433100",
        "longitude": "35.3594200",
        "approximate": False,
        "source": ("AGC Tenwek Hearts in Motion", "tenwek-hearts-in-motion", "https://heartsinmotion.tenwekhosp.org/"),
        "source_url": "https://heartsinmotion.tenwekhosp.org/",
        "corroborating_urls": ["https://kenyanathlete.com/calendar-of-events/"],
        "raw_price": "21 km categories KES 1,200",
        "price_min": 120_000,
        "price_max": 120_000,
        "tiers": (("21 km registration", 120_000),),
        "schedule_note": "Date needs organizer confirmation; arrival 5:00 AM, assembly 5:35 AM and race start 5:45 AM are official.",
    },
    {
        "rank": 7,
        "slug": "kitui-agricultural-show-trade-investment-expo-2026",
        "title": "Kitui Agricultural Show, Trade & Investment Expo 2026",
        "summary": "Three days of climate-smart agriculture, enterprise, trade and investment in Kitui.",
        "description": (
            "KASTIE 2026 is the official Kitui agricultural show and trade expo, organised with "
            "the Agricultural Society of Kenya and County Government of Kitui. Its programme "
            "includes conference sessions, demonstrations, exhibitions and networking."
        ),
        "category": "Conferences",
        "mood": "Build new connections",
        "starts_at": at(2026, 9, 24, 9, 30),
        "ends_at": at(2026, 9, 26, 17),
        "time_confirmed": True,
        "date_label": "24-26 Sep 2026",
        "organizer": "County Government of Kitui and ASK",
        "organizer_slug": "county-government-kitui-ask",
        "venue": "Ithookwe Stadium",
        "venue_slug": "ithookwe-stadium-kitui",
        "address": "Ithookwe Stadium",
        "area": "Ithookwe",
        "city": "Kitui",
        "county": "Kitui",
        "latitude": "-1.3667000",
        "longitude": "38.0167000",
        "approximate": True,
        "source": ("KASTIE official site", "kastie-official", "https://expo.codekxlabs.com/"),
        "source_url": "https://expo.codekxlabs.com/",
        "raw_price": "Registration packages on official site",
        "price_min": None,
        "price_max": None,
        "tiers": (("Official registration", 0),),
        "schedule_note": "The official programme begins with gates and registration at 9:30 AM.",
    },
    {
        "rank": 8,
        "slug": "kisima-festival-2026",
        "title": "Kisima Festival 2026 — The Love Edition",
        "summary": "Four days of African-rooted wellbeing, creativity and connection beneath Kilifi's baobabs.",
        "description": (
            "Kisima Festival returns to Beneath the Baobabs for workshops, talks, music, movement "
            "and family programming built around its 2026 theme, Love. The full pass includes "
            "festival access and camping for guests bringing their own equipment."
        ),
        "category": "Festivals",
        "mood": "Restore and connect",
        "starts_at": at(2026, 10, 16, 10),
        "ends_at": at(2026, 10, 19, 23, 59),
        "time_confirmed": True,
        "date_label": "16-19 Oct 2026",
        "organizer": "Beneath the Baobabs",
        "organizer_slug": "beneath-the-baobabs",
        "venue": "Beneath the Baobabs",
        "venue_slug": "beneath-the-baobabs-kilifi",
        "address": "Mombasa-Malindi Highway, south of Kilifi",
        "area": "Mnarani",
        "city": "Kilifi",
        "county": "Kilifi",
        "latitude": "-3.6750000",
        "longitude": "39.8490000",
        "approximate": True,
        "source": ("Quicket", "quicket", "https://www.quicket.co.ke/"),
        "source_url": "https://www.quicket.co.ke/events/341353-kisima-festival-2026/",
        "raw_price": "From KES 2,000",
        "price_min": 200_000,
        "price_max": 200_000,
        "tiers": (("Starting pass", 200_000),),
        "schedule_note": "Quicket publishes 16 October 10:00 AM to 19 October 11:59 PM.",
    },
    {
        "rank": 9,
        "slug": "women-empowerment-summit-mombasa-2026",
        "title": "Women Empowerment Summit 2026",
        "summary": "A two-day Mombasa summit focused on women, leadership, enterprise and professional connection.",
        "description": (
            "Gladeon Co. Ltd lists a two-day women empowerment summit at The Noble Ballroom in "
            "Mombasa, bringing together guests for learning, leadership and networking."
        ),
        "category": "Conferences",
        "mood": "Build new connections",
        "starts_at": at(2026, 9, 25, 9),
        "ends_at": at(2026, 9, 26, 16),
        "time_confirmed": True,
        "date_label": "25-26 Sep 2026",
        "organizer": "Gladeon Co. Ltd",
        "organizer_slug": "gladeon-co-ltd",
        "venue": "The Noble Ballroom",
        "venue_slug": "the-noble-ballroom-mombasa",
        "address": "Luhar Wadha Street",
        "area": "Mombasa Island",
        "city": "Mombasa",
        "county": "Mombasa",
        "latitude": "-4.0489700",
        "longitude": "39.6661200",
        "approximate": True,
        "source": ("TicketSasa", "ticketsasa", "https://www.ticketsasa.com/"),
        "source_url": "https://www.ticketsasa.com/events/women-empowerment-summit",
        "raw_price": "Advance KES 3,500",
        "price_min": 350_000,
        "price_max": 350_000,
        "tiers": (("Advance", 350_000),),
        "schedule_note": "TicketSasa publishes 25 September 9:00 AM to 26 September 4:00 PM.",
    },
    {
        "rank": 10,
        "slug": "migori-county-youth-summit-2026",
        "title": "Migori County Youth Summit 2026",
        "summary": "Three days of workshops, exhibitions and connections for young people across Migori County.",
        "description": (
            "Migori County Young Professionals advertises a three-day summit with networking, "
            "workshops and exhibitions, bringing together young people from the county's eight "
            "constituencies. The organizer publishes the opening time but not the final-day closing time."
        ),
        "category": "Conferences",
        "mood": "Build new connections",
        "starts_at": at(2026, 10, 28, 8),
        "ends_at": at(2026, 10, 30, 17),
        "time_confirmed": True,
        "date_label": "28-30 Oct 2026",
        "organizer": "Migori County Young Professionals",
        "organizer_slug": "migori-county-young-professionals",
        "venue": "Migori Primary School",
        "venue_slug": "migori-primary-school",
        "address": "Migori Primary School",
        "area": "Migori Town",
        "city": "Migori",
        "county": "Migori",
        "latitude": "-1.0725700",
        "longitude": "34.4689500",
        "approximate": False,
        "source": ("Migori County Young Professionals", "mcyp", "https://www.migoricountyyoungprofessionals.org/"),
        "source_url": "https://www.migoricountyyoungprofessionals.org/events/youth-summit-2026",
        "raw_price": "Price not published",
        "price_min": None,
        "price_max": None,
        "tiers": (("Registration — price not published", 0),),
        "schedule_note": "The organizer confirms an 8:00 AM opening; the final-day closing time is not published.",
    },
)


class Command(BaseCommand):
    help = "Create or update the web-verified Top 10 upcoming Kenya collection"

    @transaction.atomic
    def handle(self, *args, **options):
        if not Event.objects.filter(slug="fally-ipupa-live-in-nairobi").exists():
            call_command("upsert_fally_ipupa", verbosity=0)

        Event.objects.filter(hot_rank__isnull=False).update(hot_rank=None)
        Event.objects.filter(slug="nakuru-farmers-expo-2026").update(
            status=Event.Status.DRAFT,
            hot_rank=None,
        )
        fally = Event.objects.select_related("venue").get(slug="fally-ipupa-live-in-nairobi")
        fally.hot_rank = 5
        fally.date_confirmed = True
        fally.time_confirmed = True
        fally.save(update_fields=["hot_rank", "date_confirmed", "time_confirmed", "updated_at"])
        if fally.venue.county != "Nairobi":
            fally.venue.county = "Nairobi"
            fally.venue.save(update_fields=["county", "updated_at"])

        for item in EVENTS:
            self._upsert_event(item)

        refresh_coverage()
        self.stdout.write(
            self.style.SUCCESS(
                "Updated the 10-event Kenya collection, county coverage and source provenance."
            )
        )

    def _upsert_event(self, item):
        source_name, source_slug, source_base_url = item["source"]
        source, _ = EventSource.objects.get_or_create(
            slug=source_slug,
            defaults={
                "name": source_name,
                "base_url": source_base_url,
                "source_type": EventSource.SourceType.MANUAL,
                "adapter_name": "manual_editorial",
                "enabled": False,
                "requires_review": True,
                "auto_publish_allowed": False,
                "compliance_status": EventSource.ComplianceStatus.APPROVED_METADATA_ONLY,
                "content_usage_mode": EventSource.UsageMode.SOURCE_LINK_ONLY,
            },
        )
        organizer, _ = Organizer.objects.update_or_create(
            slug=item["organizer_slug"],
            defaults={
                "name": item["organizer"],
                "description": f"Organizer named on the {source_name} public listing.",
                "verified": False,
            },
        )
        venue, _ = Venue.objects.update_or_create(
            slug=item["venue_slug"],
            defaults={
                "name": item["venue"],
                "address": item["address"],
                "area": item["area"],
                "city": item["city"],
                "county": item["county"],
                "country": "Kenya",
                "country_code": "KE",
                "latitude": Decimal(item["latitude"]),
                "longitude": Decimal(item["longitude"]),
                "timezone": "Africa/Nairobi",
                "coordinates_are_approximate": item["approximate"],
            },
        )

        event = Event.objects.filter(slug=item["slug"]).first() or Event(slug=item["slug"])
        event.organizer = organizer
        event.venue = venue
        event.title = item["title"]
        event.summary = item["summary"]
        event.description = item["description"]
        event.category = item["category"]
        event.mood = item["mood"]
        event.status = Event.Status.PUBLISHED
        event.starts_at = item["starts_at"]
        event.ends_at = item["ends_at"]
        event.timezone = "Africa/Nairobi"
        event.time_confirmed = item["time_confirmed"]
        event.currency = "KES"
        event.featured = False
        event.hot_rank = item["rank"]
        event.date_confirmed = item.get("date_confirmed", True)
        event.selling_fast = False
        event.policies = (
            f"External listing checked 13 August 2026. {item['schedule_note']} "
            "Confirm final schedule, price, venue details and entry policy at the source: "
            f"{item['source_url']}"
        )
        if not event.cover_image and not event.external_image_url:
            event.cover_image.save(
                f"{item['slug']}-cover-pending.png",
                build_editorial_placeholder(
                    item["title"], item["county"], item["date_label"], item["rank"]
                ),
                save=False,
            )
        event.full_clean()
        event.save()

        for tier_name, price_minor in item["tiers"]:
            tier, _ = TicketTier.objects.update_or_create(
                event=event,
                name=tier_name,
                defaults={
                    "description": "External inventory; confirm current availability at the source.",
                    "price_minor": price_minor,
                    "currency": "KES",
                    "capacity": 1,
                },
            )
            tier.full_clean()
            tier.save()

        observation, _ = ScrapedEventObservation.objects.update_or_create(
            source=source,
            source_url=item["source_url"],
            defaults={
                "source_event_id": item["slug"],
                "canonical_source_url": item["source_url"],
                "raw_title": item["title"],
                "normalized_title": item["title"],
                "raw_description": "",
                "clean_description": item["description"],
                "raw_start": item["starts_at"].isoformat(),
                "raw_end": item["ends_at"].isoformat(),
                "start_at": item["starts_at"],
                "end_at": item["ends_at"],
                "timezone": "Africa/Nairobi",
                "raw_venue": item["venue"],
                "venue_name": item["venue"],
                "raw_address": item["address"],
                "address": item["address"],
                "city": item["city"],
                "county": item["county"],
                "country": "Kenya",
                "latitude": Decimal(item["latitude"]),
                "longitude": Decimal(item["longitude"]),
                "raw_category": item["category"],
                "category": item["category"],
                "raw_price": item["raw_price"],
                "price_min_minor": item["price_min"],
                "price_max_minor": item["price_max"],
                "currency": "KES",
                "is_free": item["price_min"] == 0,
                "organizer_name": item["organizer"],
                "ticket_url": item["source_url"],
                "image_url": "",
                "fingerprint": build_fingerprint(
                    item["title"], item["starts_at"], item["venue"], item["city"]
                ),
                "review_status": ScrapedEventObservation.ReviewStatus.PUBLISHED,
                "canonical_event": event,
                "retrieved_at": timezone.now(),
                "metadata": {
                    "ingestion": "manual_editorial_web_research",
                    "editorial_top_ten_rank": item["rank"],
                    "source_checked_on": "2026-08-13",
                    "schedule_note": item["schedule_note"],
                    "corroborating_sources": item.get("corroborating_urls", []),
                    "coordinates_are_approximate": item["approximate"],
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
