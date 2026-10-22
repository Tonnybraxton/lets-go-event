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
- `POST /api/orders/` (creates a reservation and starts an M-PESA STK Push)
- `GET /api/orders/<reference>/` (checkout status)
- `POST /api/payments/mpesa/callback/` (Daraja callback)

SQLite is used for local development. Set `DJANGO_USE_POSTGRES=true` and the `POSTGRES_*` variables from `.env.example` to use PostgreSQL.

## Daraja M-PESA Express (STK Push)

The checkout flow calls Daraja from Django using its REST API. Consumer credentials and the passkey stay on the Django server; the browser receives only the order/payment status. No third-party SDK package is required.

1. Create/sign in to a [Safaricom Daraja account](https://developer.safaricom.co.ke/), create a sandbox app and enable the **M-PESA Express (Lipa na M-PESA Online)** product. Copy the app's Consumer Key and Consumer Secret. Use the sandbox shortcode and passkey supplied by Daraja.
2. Copy `.env.example` to `.env` in `apps/django_admin/` and set the `MPESA_*` values there, or provide them through the Django process environment. Django loads this ignored local `.env` file at startup without overriding variables already set by the deployment. Do not expose these values with a `NEXT_PUBLIC_` prefix or commit real credentials.
3. Set `MPESA_CALLBACK_URL` to a public HTTPS address that forwards to Django's `/api/payments/mpesa/callback/` endpoint. For local testing, expose port 8000 with a temporary HTTPS tunnel (for example, ngrok) and use that tunnel URL. Safaricom requires the callback to be reachable from the internet.
4. For a PayBill, use `CustomerPayBillOnline` and set `MPESA_PARTY_B` to the PayBill shortcode. For a Till, set `MPESA_SHORTCODE` to the organization/HO shortcode, `MPESA_PARTY_B` to the Till number, and `MPESA_TRANSACTION_TYPE=CustomerBuyGoodsOnline`.
5. Apply the order payment fields and start Django:

   ```powershell
   .venv\Scripts\python.exe manage.py migrate
   .venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
   ```

For the local AURIX SHUTDOWN sandbox demo, keep `MPESA_ENV=sandbox` and run
`.venv\Scripts\python.exe manage.py enable_aurix_sandbox_checkout`. This creates
a clearly labeled KES 400 test tier and refuses to run when `MPESA_ENV=production`.
The sandbox prompt defaults to `0791677818`; it is the phone receiving the sandbox
prompt, while test payment collection goes to the configured sandbox shortcode.
This demo tier is not an official event ticket and does not represent confirmed
organizer inventory.

6. Publish an event with at least one available KES ticket tier, select tickets on its page, enter a Kenyan M-PESA number, and choose **Pay with M-PESA**. Daraja sends the STK prompt; its callback updates the order, confirms a successful payment against Daraja, and issues tickets. The browser polls the order status while the callback is processed.
7. Before going live, complete Daraja's Go Live process, use the production app credentials and passkey, set `MPESA_ENV=production`, register the production shortcode/product, and use a stable HTTPS callback URL. Test the full callback and ticket-issuance flow in sandbox first.

The integration expects a successful callback to include the paid amount, payer phone and M-PESA receipt. It also checks the CheckoutRequestID with Daraja before issuing tickets. Keep callback/status traffic on HTTPS in production and monitor/reconcile pending orders if Safaricom callbacks are delayed.

Safaricom's [M-PESA Express documentation](https://developer.safaricom.co.ke/apis/MpesaExpressSimulate) documents the STK request fields, callback payload, sandbox simulator and Go Live process.

## Let's Go Radar

Radar adds compliant source registration, staged event observations, normalization, duplicate review, county coverage and controlled publication into the existing event catalogue. Run the safe synthetic demonstration with:

```powershell
.venv\Scripts\python.exe manage.py seed_radar
.venv\Scripts\python.exe manage.py demo_radar --publish
```

See [../../docs/RADAR.md](../../docs/RADAR.md) for architecture and operations.

