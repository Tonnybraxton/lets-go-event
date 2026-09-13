import json
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Event, Order, Organizer, Ticket, TicketTier, Venue


class PublishedEventApiTests(TestCase):
    def setUp(self):
        organizer = Organizer.objects.create(
            name="Night Bloom Collective",
            slug="night-bloom-collective",
            verified=True,
        )
        venue = Venue.objects.create(
            name="Rooftop Hall",
            slug="rooftop-hall",
            address="Wood Avenue",
            area="Kilimani",
            city="Nairobi",
            county="Nairobi",
            country="Kenya",
            country_code="KE",
            latitude="-1.2929000",
            longitude="36.7854000",
        )
        starts_at = timezone.now() + timedelta(days=14)
        self.event = Event.objects.create(
            organizer=organizer,
            venue=venue,
            title="Moonlight Assembly",
            slug="moonlight-assembly",
            summary="A fictional rooftop music gathering for the catalogue API.",
            description="An original development listing.",
            category="Music",
            mood="Chill weekend",
            status=Event.Status.PUBLISHED,
            starts_at=starts_at,
            ends_at=starts_at + timedelta(hours=5),
            external_image_url="https://images.unsplash.com/photo-1506157786151-b8491531f063",
        )
        TicketTier.objects.create(
            event=self.event,
            name="General admission",
            price_minor=150000,
            currency="KES",
            capacity=100,
        )

    def test_published_event_is_returned_with_ticket_tiers(self):
        response = self.client.get(reverse("events:event-list"))
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["count"], 1)
        self.assertEqual(payload["items"][0]["slug"], "moonlight-assembly")
        self.assertEqual(payload["items"][0]["priceFromMinor"], 150000)
        self.assertEqual(payload["items"][0]["county"], "Nairobi")
        self.assertEqual(len(payload["items"][0]["ticketTiers"]), 1)

    def test_drafts_are_not_public(self):
        self.event.status = Event.Status.DRAFT
        self.event.save(update_fields=["status", "updated_at"])
        response = self.client.get(reverse("events:event-list"))
        self.assertEqual(response.json()["count"], 0)

    def test_events_can_be_filtered_by_county(self):
        response = self.client.get(reverse("events:event-list"), {"county": "Nairobi"})
        self.assertEqual(response.json()["count"], 1)
        response = self.client.get(reverse("events:event-list"), {"county": "Nakuru"})
        self.assertEqual(response.json()["count"], 0)

    def test_admin_event_add_page_is_available_to_superuser(self):
        user = get_user_model().objects.create_superuser(
            username="operations",
            email="operations@example.com",
            password="a-local-test-password",
        )
        self.client.force_login(user)
        response = self.client.get(reverse("admin:events_event_add"))
        self.assertEqual(response.status_code, 200)

    def test_ticket_reservation_updates_inventory(self):
        tier = self.event.ticket_tiers.get()
        response = self.client.post(
            reverse("events:order-create"),
            data=json.dumps({"items": [{"tierId": str(tier.id), "quantity": 2}]}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["status"], Order.Status.RESERVED)
        tier.refresh_from_db()
        self.assertEqual(tier.reserved_count, 2)

    def test_paid_ticket_can_only_be_checked_in_once(self):
        tier = self.event.ticket_tiers.get()
        order = Order.objects.create(
            event=self.event,
            status=Order.Status.PAID,
            total_minor=tier.price_minor,
            currency="KES",
            reservation_expires_at=timezone.now() + timedelta(minutes=10),
        )
        ticket = Ticket.objects.create(order=order, tier=tier)
        payload = json.dumps({"code": ticket.code})
        first = self.client.post(reverse("events:scanner-scan"), data=payload, content_type="application/json")
        second = self.client.post(reverse("events:scanner-scan"), data=payload, content_type="application/json")
        self.assertEqual(first.status_code, 200)
        self.assertTrue(first.json()["valid"])
        self.assertEqual(second.status_code, 409)
