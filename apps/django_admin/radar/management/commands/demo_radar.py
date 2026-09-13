from django.core.management.base import BaseCommand

from radar.models import EventSource
from radar.models import ScrapedEventObservation
from radar.services.pipeline import publish_observation
from radar.services.runs import ingest_document


DEMO_HTML = """
<!doctype html><html><head><script type="application/ld+json">
{
  "@context": "https://schema.org", "@type": "MusicEvent",
  "@id": "demo:nairobi-rooftop-sessions",
  "name": "Nairobi Rooftop Sessions",
  "description": "A fictional safe Radar demonstration featuring live Kenyan soul and skyline views.",
  "startDate": "2026-11-14T17:00:00+03:00", "endDate": "2026-11-14T23:00:00+03:00",
  "url": "https://demo.letsgo.invalid/events/nairobi-rooftop-sessions",
  "image": "https://images.unsplash.com/photo-1506157786151-b8491531f063?auto=format&fit=crop&w=1600&q=85",
  "location": {"@type": "Place", "name": "Skyline Demo Deck", "address": {
    "@type": "PostalAddress", "streetAddress": "Wood Avenue", "addressLocality": "Nairobi",
    "addressRegion": "Nairobi", "addressCountry": "Kenya"}},
  "organizer": {"@type": "Organization", "name": "Let's Go Radar Demo"},
  "offers": {"@type": "Offer", "price": "1500", "priceCurrency": "KES",
    "url": "https://demo.letsgo.invalid/tickets/nairobi-rooftop-sessions"}
}
</script></head><body><h1>Synthetic Radar fixture</h1></body></html>
"""


class Command(BaseCommand):
    help = "Run the complete Radar pipeline against a safe synthetic JSON-LD fixture"

    def add_arguments(self, parser):
        parser.add_argument(
            "--publish",
            action="store_true",
            help="Publish the resulting high-quality observation into the canonical event catalogue.",
        )

    def handle(self, *args, **options):
        source, _ = EventSource.objects.update_or_create(
            slug="synthetic-jsonld-feed",
            defaults={
                "name": "Synthetic JSON-LD Feed",
                "base_url": "https://demo.letsgo.invalid/",
                "source_type": EventSource.SourceType.JSON_LD,
                "adapter_name": "generic_jsonld",
                "enabled": True,
                "compliance_status": EventSource.ComplianceStatus.PARTNER,
                "content_usage_mode": EventSource.UsageMode.FULL_PARTNER_CONTENT,
                "requires_review": True,
                "trust_level": 100,
            },
        )
        run = ingest_document(source, DEMO_HTML, source.base_url)
        if options["publish"]:
            observation = ScrapedEventObservation.objects.filter(run=run).first()
            if observation:
                event = publish_observation(observation)
                self.stdout.write(self.style.SUCCESS(f"Published canonical event: {event.title}"))
        self.stdout.write(self.style.SUCCESS(f"Radar run {run.id} created {run.observations_created} observation(s)."))
