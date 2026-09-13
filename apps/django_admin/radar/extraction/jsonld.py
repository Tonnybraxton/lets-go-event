import json
from collections.abc import Iterable
from typing import Any
from urllib.parse import urljoin

from parsel import Selector

from radar.domain import RawEventObservation
from radar.extraction.base import ExtractionStrategy


EVENT_TYPES = {
    "Event",
    "MusicEvent",
    "BusinessEvent",
    "SportsEvent",
    "EducationEvent",
    "Festival",
    "TheaterEvent",
    "SocialEvent",
    "ExhibitionEvent",
}


def _nodes(value: Any) -> Iterable[dict[str, Any]]:
    if isinstance(value, list):
        for item in value:
            yield from _nodes(item)
    elif isinstance(value, dict):
        if "@graph" in value:
            yield from _nodes(value["@graph"])
        yield value


def _first(value: Any) -> Any:
    return value[0] if isinstance(value, list) and value else value


def _name(value: Any) -> str:
    value = _first(value)
    if isinstance(value, dict):
        return str(value.get("name", ""))
    return str(value or "")


def _image(value: Any) -> str:
    value = _first(value)
    if isinstance(value, dict):
        return str(value.get("url", ""))
    return str(value or "")


class JsonLdExtractor(ExtractionStrategy):
    def extract(self, document: str, source_url: str) -> list[RawEventObservation]:
        observations: list[RawEventObservation] = []
        selector = Selector(text=document)
        for raw_script in selector.css('script[type="application/ld+json"]::text').getall():
            try:
                payload = json.loads(raw_script)
            except (json.JSONDecodeError, TypeError):
                continue
            for node in _nodes(payload):
                node_types = node.get("@type", [])
                if isinstance(node_types, str):
                    node_types = [node_types]
                if not EVENT_TYPES.intersection(node_types):
                    continue
                location = _first(node.get("location", {})) or {}
                if not isinstance(location, dict):
                    location = {}
                address = location.get("address", {})
                if isinstance(address, str):
                    address = {"streetAddress": address}
                offers = _first(node.get("offers", {})) or {}
                if not isinstance(offers, dict):
                    offers = {}
                event_url = str(node.get("url") or source_url)
                observations.append(
                    RawEventObservation(
                        source_url=urljoin(source_url, event_url),
                        source_event_id=str(node.get("@id", "")),
                        title=str(node.get("name", "")).strip(),
                        description=str(node.get("description", "")).strip(),
                        start_raw=str(node.get("startDate", "")),
                        end_raw=str(node.get("endDate", "")),
                        venue_raw=_name(location),
                        address_raw=str(address.get("streetAddress", "")),
                        city_raw=str(address.get("addressLocality", "")),
                        county_raw=str(address.get("addressRegion", "")),
                        country_raw=_name(address.get("addressCountry")) or "Kenya",
                        organizer_raw=_name(node.get("organizer")),
                        category_raw=str(node.get("eventType", "")),
                        price_raw=str(offers.get("price", "")),
                        currency_raw=str(offers.get("priceCurrency", "KES")),
                        ticket_url=urljoin(source_url, str(offers.get("url", ""))),
                        image_url=urljoin(source_url, _image(node.get("image"))),
                        status_raw=str(node.get("eventStatus", "")),
                        metadata={"schema_types": node_types},
                    )
                )
        return [item for item in observations if item.title]
