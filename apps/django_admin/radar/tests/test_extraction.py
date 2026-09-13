from django.test import SimpleTestCase

from radar.extraction import JsonLdExtractor, SelectorExtractor
from radar.security import validate_public_url


class ExtractorTests(SimpleTestCase):
    def test_jsonld_event_is_extracted(self):
        html = '''<script type="application/ld+json">{
          "@context":"https://schema.org","@type":"MusicEvent","name":"Kenya AI Builders Meetup",
          "startDate":"2026-12-04T18:00:00+03:00","location":{"name":"Demo Hall",
          "address":{"addressLocality":"Nairobi","addressRegion":"Nairobi"}}
        }</script>'''
        result = JsonLdExtractor().extract(html, "https://example.org/events")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].title, "Kenya AI Builders Meetup")

    def test_configurable_css_adapter(self):
        html = '<article class="event"><h2>Coast Culture Weekend</h2><time>2026-12-10</time></article>'
        result = SelectorExtractor({"listing_selector": ".event", "fields": {
            "title": "h2::text", "start_raw": "time::text"
        }}).extract(html, "https://example.org/events")
        self.assertEqual(result[0].title, "Coast Culture Weekend")

    def test_private_source_is_rejected(self):
        with self.assertRaisesMessage(Exception, "private"):
            validate_public_url("http://127.0.0.1/")
