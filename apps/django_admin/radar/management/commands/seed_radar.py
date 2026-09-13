from django.core.management.base import BaseCommand

from radar.models import EventSource
from radar.tasks import refresh_coverage


CANDIDATES = [
    ("TicketSasa", "https://ticketsasa.com/"),
    ("KenyaBuzz", "https://www.kenyabuzz.com/"),
    ("MOOKH", "https://mookh.com/"),
    ("Tickets Kenya", "https://ticketskenya.com/"),
]


class Command(BaseCommand):
    help = "Seed disabled Kenyan source candidates and all 47 county coverage records"

    def handle(self, *args, **options):
        for name, url in CANDIDATES:
            EventSource.objects.update_or_create(
                slug=name.lower().replace(" ", "-"),
                defaults={
                    "name": name,
                    "base_url": url,
                    "source_type": EventSource.SourceType.OTHER,
                    "enabled": False,
                    "compliance_status": EventSource.ComplianceStatus.NOT_REVIEWED,
                    "content_usage_mode": EventSource.UsageMode.DISABLED_PENDING_REVIEW,
                    "adapter_name": "configuration_required",
                },
            )
        refresh_coverage()
        self.stdout.write(self.style.SUCCESS("Seeded Radar candidates and 47-county coverage."))
