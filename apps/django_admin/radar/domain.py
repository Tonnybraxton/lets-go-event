from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class RawEventObservation:
    source_url: str
    title: str
    source_event_id: str = ""
    description: str = ""
    start_raw: str = ""
    end_raw: str = ""
    venue_raw: str = ""
    address_raw: str = ""
    city_raw: str = ""
    county_raw: str = ""
    country_raw: str = "Kenya"
    organizer_raw: str = ""
    category_raw: str = ""
    price_raw: str = ""
    currency_raw: str = "KES"
    ticket_url: str = ""
    image_url: str = ""
    status_raw: str = ""
    latitude_raw: str = ""
    longitude_raw: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    retrieved_at: datetime | None = None

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)
