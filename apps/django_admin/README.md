# Let's Go Event Django admin

This service is the editorial catalogue for organizers, venues, events, artwork, schedules and ticket tiers. Published events are exposed through a read-only JSON API and merged into the customer-facing Next.js catalogue.

## Local admin login

- URL: `http://127.0.0.1:8000/admin/`

Create your own local administrator using the setup commands below. Credentials and the local database are not included in the repository.

## Local setup

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe manage.py migrate
$env:DJANGO_ADMIN_PASSWORD = "choose-a-strong-password"
.venv\Scripts\python.exe manage.py bootstrap_admin --username operations --email operations@letsgo.local
.venv\Scripts\python.exe manage.py seed_catalogue
.venv\Scripts\python.exe manage.py seed_top_kenya_events
.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
```

Open `http://127.0.0.1:8000/admin/`. An event is visible to the customer application only when its status is **Published**. Add at least one ticket tier and either upload a cover image or provide an external image URL.

`seed_top_kenya_events` idempotently loads the web-researched Top 10 collection, county metadata, source links and neutral covers awaiting editorial artwork. It deliberately leaves every external source crawler disabled.

The public endpoints are:

- `GET /api/health/`
- `GET /api/events/`
- `GET /api/events/<slug>/`

SQLite is used for local development. Set `DJANGO_USE_POSTGRES=true` and the `POSTGRES_*` variables from `.env.example` to use PostgreSQL.

## Let's Go Radar

Radar adds compliant source registration, staged event observations, normalization, duplicate review, county coverage and controlled publication into the existing event catalogue. Run the safe synthetic demonstration with:

```powershell
.venv\Scripts\python.exe manage.py seed_radar
.venv\Scripts\python.exe manage.py demo_radar --publish
```

See [../../docs/RADAR.md](../../docs/RADAR.md) for architecture and operations.
