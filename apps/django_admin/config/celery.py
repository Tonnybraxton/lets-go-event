import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("lets_go_event")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
app.conf.beat_schedule = {
    "radar-discover-due-sources": {
        "task": "radar.discover_due_sources",
        "schedule": 300.0,
    }
}
