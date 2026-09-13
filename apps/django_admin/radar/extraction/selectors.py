from urllib.parse import urljoin

from parsel import Selector

from radar.domain import RawEventObservation
from radar.extraction.base import ExtractionStrategy


class SelectorExtractor(ExtractionStrategy):
    ALLOWED_FIELDS = {
        "title",
        "description",
        "start_raw",
        "end_raw",
        "venue_raw",
        "address_raw",
        "city_raw",
        "county_raw",
        "organizer_raw",
        "category_raw",
        "price_raw",
        "ticket_url",
        "image_url",
    }

    def __init__(self, config: dict):
        self.config = config

    @staticmethod
    def _select(selector: Selector, expression: str) -> str:
        if expression.startswith("xpath:"):
            return (selector.xpath(expression.removeprefix("xpath:")).get() or "").strip()
        return (selector.css(expression).get() or "").strip()

    def extract(self, document: str, source_url: str) -> list[RawEventObservation]:
        root = Selector(text=document)
        listing = self.config.get("listing_selector")
        cards = root.css(listing) if listing else [root]
        fields = self.config.get("fields", {})
        observations: list[RawEventObservation] = []
        for card in cards:
            values = {
                key: self._select(card, expression)
                for key, expression in fields.items()
                if key in self.ALLOWED_FIELDS and isinstance(expression, str)
            }
            link_selector = self.config.get("detail_link_selector", "")
            event_url = self._select(card, link_selector) if link_selector else source_url
            values["ticket_url"] = urljoin(source_url, values.get("ticket_url", ""))
            values["image_url"] = urljoin(source_url, values.get("image_url", ""))
            observation = RawEventObservation(source_url=urljoin(source_url, event_url), **values)
            if observation.title:
                observations.append(observation)
        return observations
