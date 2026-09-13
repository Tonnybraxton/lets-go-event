# Radar operations

Celery uses Redis database 0 for the broker and database 1 for results. Beat checks due sources every five minutes. A due source creates a queued Radar Run; a worker/adapter executes only compliance-approved sources.

```powershell
cd apps\django_admin
.venv\Scripts\celery.exe -A config worker -l info
.venv\Scripts\celery.exe -A config beat -l info
```

Monitor source failure count, last success, health status, run correlation ID, parser anomalies, and observation volume. Parser failures preserve previously published events. Selector changes require fixture tests and review; Radar never rewrites spiders autonomously.
