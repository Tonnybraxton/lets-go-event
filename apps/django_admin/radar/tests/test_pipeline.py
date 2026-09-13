from django.test import TestCase

from radar.models import EventSource, ScrapedEventObservation
from radar.services.runs import ingest_document


HTML = '''<script type="application/ld+json">{
"@context":"https://schema.org","@type":"Event","name":"Nakuru Family Adventure Day",
"description":"A fictional family day for safe pipeline testing.",
"startDate":"2026-12-12T09:00:00+03:00","endDate":"2026-12-12T17:00:00+03:00",
"url":"https://example.org/events/family-day","location":{"name":"Demo Gardens",
"address":{"streetAddress":"Garden Road","addressLocality":"Nakuru","addressRegion":"Nakuru"}},
"organizer":{"name":"Demo Organizer"},"offers":{"price":"500","priceCurrency":"KES"}
}</script>'''


class RadarPipelineTests(TestCase):
    def setUp(self):
        self.source = EventSource.objects.create(
            name="Approved Fixture", slug="approved-fixture", base_url="https://example.org/",
            source_type="JSON_LD", adapter_name="generic_jsonld", enabled=True,
            compliance_status="PARTNER", content_usage_mode="FULL_PARTNER_CONTENT",
        )

    def test_document_is_staged_and_normalized(self):
        run = ingest_document(self.source, HTML, self.source.base_url)
        self.assertEqual(run.observations_created, 1)
        observation = ScrapedEventObservation.objects.get()
        self.assertEqual(observation.county, "Nakuru")
        self.assertEqual(observation.price_min_minor, 50000)
        self.assertGreaterEqual(observation.quality_score, 60)

    def test_unreviewed_source_is_blocked(self):
        self.source.enabled = False
        self.source.compliance_status = "NOT_REVIEWED"
        self.source.save()
        run = ingest_document(self.source, HTML, self.source.base_url)
        self.assertEqual(run.status, "BLOCKED")
        self.assertFalse(ScrapedEventObservation.objects.exists())
