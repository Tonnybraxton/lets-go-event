from datetime import datetime
from decimal import Decimal
from zoneinfo import ZoneInfo

from django.core.management.base import BaseCommand

from events.models import Event, Organizer, TicketTier, Venue


class Command(BaseCommand):
    help = "Create or update the development catalogue event"

    def handle(self, *args, **options):
        organizer, _ = Organizer.objects.update_or_create(
            slug="night-bloom-collective",
            defaults={
                "name": "Night Bloom Collective",
                "description": "Independent producers of intimate Nairobi music experiences.",
                "verified": True,
            },
        )
        venue, _ = Venue.objects.update_or_create(
            slug="rooftop-hall-kilimani",
            defaults={
                "name": "Rooftop Hall",
                "address": "Wood Avenue",
                "area": "Kilimani",
                "city": "Nairobi",
                "country": "Kenya",
                "country_code": "KE",
                "latitude": Decimal("-1.2929000"),
                "longitude": Decimal("36.7854000"),
                "timezone": "Africa/Nairobi",
            },
        )
        nairobi = ZoneInfo("Africa/Nairobi")
        event, created = Event.objects.update_or_create(
            slug="moonlight-assembly",
            defaults={
                "organizer": organizer,
                "venue": venue,
                "title": "Moonlight Assembly",
                "summary": "A rooftop gathering shaped by live soul, soft light and Nairobi after dark.",
                "description": (
                    "An intimate evening of original live performances, small plates and a panoramic "
                    "city view. This development listing can be edited safely from Django admin."
                ),
                "category": "Music",
                "mood": "Chill weekend",
                "status": Event.Status.PUBLISHED,
                "starts_at": datetime(2026, 10, 10, 17, 30, tzinfo=nairobi),
                "ends_at": datetime(2026, 10, 10, 23, 30, tzinfo=nairobi),
                "timezone": "Africa/Nairobi",
                "currency": "KES",
                "external_image_url": (
                    "https://images.unsplash.com/photo-1506157786151-b8491531f063"
                    "?auto=format&fit=crop&w=1800&q=88"
                ),
                "featured": True,
                "selling_fast": False,
                "age_restriction": "18+",
            },
        )
        TicketTier.objects.update_or_create(
            event=event,
            name="General admission",
            defaults={
                "description": "Entry from 5:30 PM",
                "price_minor": 150000,
                "currency": "KES",
                "capacity": 160,
            },
        )
        action = "Created" if created else "Updated"
        self.stdout.write(self.style.SUCCESS(f"{action} Moonlight Assembly."))
