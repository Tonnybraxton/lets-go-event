from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from radar.models import EventSource, ScrapeRun


@shared_task(name="radar.discover_due_sources")
def discover_due_sources() -> dict[str, int]:
    now = timezone.now()
    due = 0
    queued = 0
    for source in EventSource.objects.filter(enabled=True):
        threshold = now - timedelta(minutes=source.crawl_frequency_minutes)
        if not source.last_successful_run_at or source.last_successful_run_at <= threshold:
            due += 1
            if source.may_crawl:
                ScrapeRun.objects.create(source=source, status=ScrapeRun.Status.QUEUED)
                queued += 1
    return {"due": due, "queued": queued}


@shared_task(name="radar.refresh_coverage")
def refresh_coverage() -> int:
    from django.db.models import Count
    from events.models import Event
    from radar.geography import KENYA_COUNTIES
    from radar.models import CountyCoverage

    now = timezone.now()
    updated = 0
    for county in KENYA_COUNTIES:
        events = Event.objects.filter(
            status=Event.Status.PUBLISHED,
            starts_at__gte=now,
            venue__county__iexact=county,
        )
        count = events.count()
        categories = list(events.values_list("category", flat=True).distinct())
        active_sources = sum(
            1
            for source in EventSource.objects.filter(enabled=True).only("adapter_config")
            if county in source.adapter_config.get("counties", [])
        )
        recommendation = ""
        if count == 0 and active_sources == 0:
            recommendation = f"No known future events or active county-specific sources. Find and review public or partner sources for {county}."
        CountyCoverage.objects.update_or_create(
            county=county,
            defaults={
                "known_upcoming_events": count,
                "active_sources": active_sources,
                "categories_represented": categories,
                "last_discovery_at": now,
                "gap_recommendation": recommendation,
            },
        )
        updated += 1
    return updated
