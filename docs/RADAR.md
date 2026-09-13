# Let's Go Radar

Let's Go Radar is the event-intelligence ingestion layer for Let's Go Event. It discovers public or partner-provided event metadata, stages immutable source observations, normalizes them, checks quality and likely duplicates, then sends them to Django Admin for review. Only the publishing service creates records in the existing canonical `events.Event` catalogue.

Pipeline: Source Registry → Radar Run → extractor → observation → normalization → quality → duplicate review → approval → canonical event.

Radar never claims complete knowledge of Kenyan events. Coverage records show known events and identified source gaps.

## Safe demo

```powershell
cd apps\django_admin
.venv\Scripts\python.exe manage.py seed_radar
.venv\Scripts\python.exe manage.py demo_radar --publish
```

Open Django Admin and select **Let's Go Radar → Scraped event observations**.
