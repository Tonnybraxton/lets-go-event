import os
from datetime import datetime
from decimal import Decimal
from zoneinfo import ZoneInfo

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from events.models import Event, Organizer, TicketTier, Venue


class Command(BaseCommand):
    help = "Create the clearly labeled Aurix sandbox checkout demo (never for production sales)."

    @transaction.atomic
    def handle(self, *args, **options):
        if os.getenv("MPESA_ENV", "").strip().lower() != "sandbox":
            raise CommandError("This demo checkout is sandbox-only. Set MPESA_ENV=sandbox to enable it.")

        organizer, _ = Organizer.objects.update_or_create(
            slug="aurix-inc",
            defaults={
                "name": "aurix.inc",
                "description": "Organizer named on the public AURIX SHUTDOWN listing.",
                "verified": False,
            },
        )
        venue, _ = Venue.objects.update_or_create(
            slug="event-space-amee-arcade-westlands",
            defaults={
                "name": "The Event Space, Amee Arcade",
                "address": "Parklands Road",
                "area": "Westlands",
                "city": "Nairobi",
                "county": "Nairobi",
                "country": "Kenya",
                "country_code": "KE",
                "latitude": Decimal("-1.2623000"),
                "longitude": Decimal("36.8021000"),
                "timezone": "Africa/Nairobi",
                "coordinates_are_approximate": True,
            },
        )
        nairobi = ZoneInfo("Africa/Nairobi")
        event, created = Event.objects.update_or_create(
            slug="aurix-shutdown",
            defaults={
                "organizer": organizer,
                "venue": venue,
                "title": "AURIX SHUTDOWN",
                "summary": "A Nairobi music event at The Event Space in Westlands.",
                "description": (
                    "This local event record exists only to exercise the Daraja sandbox checkout. "
                    "The external listing reports tickets from KES 400. This sandbox tier is not "
                    "an official ticket and does not guarantee event access. Confirm real inventory "
                    "and resale authorization with the organizer before offering live checkout."
                ),
                "category": "Music",
                "mood": "Dance all night",
                "status": Event.Status.PUBLISHED,
                "starts_at": datetime(2026, 12, 15, 16, 0, tzinfo=nairobi),
                "ends_at": datetime(2026, 12, 15, 23, 0, tzinfo=nairobi),
                "timezone": "Africa/Nairobi",
                "currency": "KES",
                "external_image_url": "https://lipatix.com/organizer_dashboard/uploads/event_posters/event_218_6cbd0403f6a6fda961838d507b9bbd90_1787674669.png",
                "date_confirmed": True,
                "time_confirmed": True,
                "age_restriction": "18+",
            },
        )
        TicketTier.objects.update_or_create(
            event=event,
            name="Sandbox entry (test only)",
            defaults={
                "description": "Test inventory only; no official event ticket is issued.",
                "price_minor": 40000,
                "currency": "KES",
                "capacity": 20,
            },
        )

        action = "Created" if created else "Updated"
        self.stdout.write(self.style.SUCCESS(f"{action} AURIX SHUTDOWN sandbox checkout."))

