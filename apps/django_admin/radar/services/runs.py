from django.db import transaction
from django.utils import timezone

from radar.domain import RawEventObservation
from radar.extraction import JsonLdExtractor, SelectorExtractor
from radar.models import EventSource, ScrapeRun
from radar.services.pipeline import ingest_raw


@transaction.atomic
def ingest_document(source: EventSource, document: str, source_url: str) -> ScrapeRun:
    if not source.may_crawl:
        return ScrapeRun.objects.create(
            source=source,
            status=ScrapeRun.Status.BLOCKED,
            started_at=timezone.now(),
            finished_at=timezone.now(),
            safe_error_message="Source is disabled or has not passed compliance review.",
        )
    run = ScrapeRun.objects.create(
        source=source, status=ScrapeRun.Status.RUNNING, started_at=timezone.now(), pages_requested=1
    )
    extractor = (
        SelectorExtractor(source.adapter_config)
        if source.adapter_name == "generic_selectors"
        else JsonLdExtractor()
    )
    observations = extractor.extract(document, source_url)
    for raw in observations:
        ingest_raw(source, raw, run)
    run.status = ScrapeRun.Status.SUCCEEDED
    run.finished_at = timezone.now()
    run.pages_succeeded = 1
    run.observations_created = len(observations)
    run.save()
    source.last_successful_run_at = run.finished_at
    source.failure_count = 0
    source.health_status = EventSource.HealthStatus.HEALTHY
    source.save(update_fields=["last_successful_run_at", "failure_count", "health_status", "updated_at"])
    return run


def ingest_raw_items(source: EventSource, items: list[RawEventObservation]) -> ScrapeRun:
    run = ScrapeRun.objects.create(
        source=source, status=ScrapeRun.Status.RUNNING, started_at=timezone.now()
    )
    for item in items:
        ingest_raw(source, item, run)
    run.status = ScrapeRun.Status.SUCCEEDED
    run.finished_at = timezone.now()
    run.observations_created = len(items)
    run.save()
    return run
