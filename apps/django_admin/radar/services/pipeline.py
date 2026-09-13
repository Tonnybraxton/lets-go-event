import hashlib
import re
from datetime import timedelta
from decimal import Decimal, InvalidOperation
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import dateparser
from django.db import transaction
from django.utils import timezone
from django.utils.text import slugify
from rapidfuzz.fuzz import token_set_ratio

from events.models import Event, Organizer, TicketTier, Venue
from radar.domain import RawEventObservation
from radar.geography import resolve_county
from radar.models import DuplicateCandidate, EventSource, ScrapeRun, ScrapedEventObservation
from radar.security import TRACKING_PARAMETERS, validate_public_url


def normalize_title(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def canonicalize_url(value: str) -> str:
    safe = validate_public_url(value)
    parsed = urlsplit(safe)
    query = urlencode(
        [(key, item) for key, item in parse_qsl(parsed.query) if key.casefold() not in TRACKING_PARAMETERS]
    )
    path = parsed.path.rstrip("/") or "/"
    return urlunsplit((parsed.scheme.lower(), parsed.netloc.lower(), path, query, ""))


def parse_datetime(value: str):
    if not value:
        return None
    parsed = dateparser.parse(
        value,
        settings={"TIMEZONE": "Africa/Nairobi", "RETURN_AS_TIMEZONE_AWARE": True},
    )
    return parsed


def parse_price(value: str) -> tuple[int | None, bool]:
    if not value:
        return None, False
    if "free" in value.casefold():
        return 0, True
    matches = re.findall(r"\d[\d,]*(?:\.\d+)?", value)
    if not matches:
        return None, False
    try:
        amount = Decimal(matches[0].replace(",", ""))
    except InvalidOperation:
        return None, False
    return max(0, int(amount * 100)), amount == 0


def build_fingerprint(title: str, start_at, venue: str, city: str) -> str:
    date_value = start_at.date().isoformat() if start_at else "unknown"
    material = "|".join(
        [slugify(title), date_value, slugify(venue), slugify(city)]
    )
    return hashlib.sha256(material.encode("utf-8")).hexdigest()


def quality_score(observation: ScrapedEventObservation) -> tuple[int, list[str]]:
    score = 0
    issues: list[str] = []
    fields = [
        (observation.normalized_title, 20, "missing title"),
        (observation.start_at, 20, "missing/invalid start date"),
        (observation.venue_name, 12, "missing venue"),
        (observation.city, 10, "missing city"),
        (observation.county, 10, "unresolved county"),
        (observation.clean_description, 8, "missing description"),
        (observation.image_url, 5, "missing image"),
        (observation.organizer_name, 5, "missing organizer"),
        (observation.category, 5, "missing category"),
        (observation.source_url, 5, "missing source URL"),
    ]
    for value, points, issue in fields:
        if value:
            score += points
        else:
            issues.append(issue)
    if observation.end_at and observation.start_at and observation.end_at <= observation.start_at:
        score = max(0, score - 25)
        issues.append("end date is not after start date")
    return min(score, 100), issues


def find_duplicate_candidates(observation: ScrapedEventObservation) -> list[DuplicateCandidate]:
    if not observation.start_at:
        return []
    window_start = observation.start_at - timedelta(days=1)
    window_end = observation.start_at + timedelta(days=1)
    candidates = Event.objects.filter(starts_at__range=(window_start, window_end)).select_related("venue")
    results: list[DuplicateCandidate] = []
    for event in candidates:
        title_score = token_set_ratio(observation.normalized_title, event.title)
        venue_score = token_set_ratio(observation.venue_name, event.venue.name)
        score = Decimal(str(round(title_score * 0.75 + venue_score * 0.25, 2)))
        if score >= Decimal("72"):
            result, _ = DuplicateCandidate.objects.update_or_create(
                observation=observation,
                candidate_event=event,
                defaults={"score": score, "reasons": ["similar title", "near date", "similar venue"]},
            )
            results.append(result)
    return results


@transaction.atomic
def ingest_raw(source: EventSource, raw: RawEventObservation, run: ScrapeRun | None = None):
    source_url = canonicalize_url(raw.source_url)
    start_at = parse_datetime(raw.start_raw)
    end_at = parse_datetime(raw.end_raw)
    price_minor, is_free = parse_price(raw.price_raw)
    county = resolve_county(raw.city_raw, raw.county_raw, raw.address_raw)
    title = normalize_title(raw.title)
    defaults = {
        "run": run,
        "source_event_id": raw.source_event_id,
        "canonical_source_url": source_url,
        "raw_title": raw.title,
        "normalized_title": title,
        "raw_description": raw.description,
        "clean_description": re.sub(r"\s+", " ", raw.description).strip(),
        "raw_start": raw.start_raw,
        "raw_end": raw.end_raw,
        "start_at": start_at,
        "end_at": end_at,
        "raw_venue": raw.venue_raw,
        "venue_name": normalize_title(raw.venue_raw),
        "raw_address": raw.address_raw,
        "address": normalize_title(raw.address_raw),
        "city": normalize_title(raw.city_raw),
        "county": county,
        "country": raw.country_raw or "Kenya",
        "raw_category": raw.category_raw,
        "category": source.default_category or normalize_title(raw.category_raw) or "Experiences",
        "raw_price": raw.price_raw,
        "price_min_minor": price_minor,
        "price_max_minor": price_minor,
        "currency": (raw.currency_raw or "KES")[:3].upper(),
        "is_free": is_free,
        "organizer_name": normalize_title(raw.organizer_raw),
        "ticket_url": raw.ticket_url,
        "image_url": raw.image_url,
        "fingerprint": build_fingerprint(title, start_at, raw.venue_raw, raw.city_raw),
        "metadata": raw.metadata,
        "retrieved_at": raw.retrieved_at or timezone.now(),
        "review_status": ScrapedEventObservation.ReviewStatus.NORMALIZED,
    }
    observation, _ = ScrapedEventObservation.objects.update_or_create(
        source=source, source_url=source_url, defaults=defaults
    )
    observation.quality_score, observation.validation_issues = quality_score(observation)
    observation.review_status = (
        ScrapedEventObservation.ReviewStatus.NEEDS_REVIEW
        if observation.validation_issues or source.requires_review
        else ScrapedEventObservation.ReviewStatus.APPROVED
    )
    observation.save(update_fields=["quality_score", "validation_issues", "review_status", "updated_at"])
    find_duplicate_candidates(observation)
    return observation


def unique_slug(model, value: str) -> str:
    base = slugify(value)[:140] or "radar-event"
    candidate = base
    suffix = 2
    while model.objects.filter(slug=candidate).exists():
        candidate = f"{base[:130]}-{suffix}"
        suffix += 1
    return candidate


@transaction.atomic
def publish_observation(observation: ScrapedEventObservation) -> Event:
    if observation.canonical_event_id:
        return observation.canonical_event
    if observation.quality_score < 60 or not observation.start_at:
        raise ValueError("Observation must have a valid date and quality score of at least 60.")
    organizer_name = observation.organizer_name or f"{observation.source.name} listing"
    organizer, _ = Organizer.objects.get_or_create(
        name=organizer_name,
        defaults={"slug": unique_slug(Organizer, organizer_name), "verified": False},
    )
    venue_name = observation.venue_name or "Venue to be confirmed"
    venue = Venue.objects.filter(name=venue_name, city=observation.city).first()
    if not venue:
        venue = Venue.objects.create(
            name=venue_name,
            slug=unique_slug(Venue, f"{venue_name}-{observation.city}"),
            address=observation.address or "See source for venue details",
            city=observation.city or "Kenya",
            county=observation.county,
            country=observation.country,
            latitude=observation.latitude or Decimal("0"),
            longitude=observation.longitude or Decimal("0"),
        )
    event = Event.objects.create(
        organizer=organizer,
        venue=venue,
        title=observation.normalized_title,
        slug=unique_slug(Event, observation.normalized_title),
        summary=(observation.clean_description or f"Event discovered by {observation.source.name}.")[:240],
        description=observation.clean_description or "See the original source for event details.",
        category=observation.category if observation.category in dict(Event.CATEGORIES) else "Experiences",
        mood="Discover something new",
        status=Event.Status.PUBLISHED,
        starts_at=observation.start_at,
        ends_at=observation.end_at or observation.start_at + timedelta(hours=3),
        currency=observation.currency,
        external_image_url=observation.image_url,
        policies=f"Source: {observation.source_url}",
    )
    TicketTier.objects.create(
        event=event,
        name="Source listing",
        description="Complete booking on the original event source",
        price_minor=observation.price_min_minor or 0,
        currency=observation.currency,
        capacity=1,
    )
    observation.canonical_event = event
    observation.review_status = ScrapedEventObservation.ReviewStatus.PUBLISHED
    observation.save(update_fields=["canonical_event", "review_status", "updated_at"])
    return event
