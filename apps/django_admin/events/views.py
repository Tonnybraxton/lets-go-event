import json
import re
from datetime import timedelta
from decimal import Decimal, InvalidOperation

from django.db import transaction
from django.db.models import F, Prefetch
from django.http import Http404, JsonResponse
from django.utils import timezone
from django.utils.text import slugify
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from .models import Event, LocationSuggestion, Order, OrderItem, Organizer, Ticket, TicketTier, Venue
from .daraja import DarajaError, initiate_stk_push, query_stk_push


def _payload(request):
    try:
        return json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return None


def _error(message: str, status: int = 400):
    return JsonResponse({"error": message}, status=status)


def _image_url(request, event: Event) -> str:
    if event.cover_image:
        return request.build_absolute_uri(event.cover_image.url)
    return event.external_image_url


def _normalize_mpesa_phone(value) -> str | None:
    digits = re.sub(r"\D", "", str(value or ""))
    if digits.startswith("0") and len(digits) == 10:
        digits = "254" + digits[1:]
    elif digits.startswith("7") or digits.startswith("1"):
        digits = "254" + digits
    return digits if re.fullmatch(r"254[17]\d{8}", digits) else None


def _serialize_event(request, event: Event) -> dict:
    tiers = list(event.ticket_tiers.all())
    radar_observation = next(iter(event.radar_observations.all()), None)
    price_available = radar_observation.price_min_minor is not None if radar_observation else bool(tiers)
    return {
        "id": str(event.id),
        "slug": event.slug,
        "title": event.title,
        "summary": event.summary,
        "description": event.description,
        "category": event.category,
        "mood": event.mood or "Discover something new",
        "image": _image_url(request, event),
        "startAt": event.starts_at.isoformat(),
        "endAt": event.ends_at.isoformat(),
        "timezone": event.timezone,
        "venue": event.venue.name,
        "address": event.venue.address,
        "area": event.venue.area,
        "city": event.venue.city,
        "county": event.venue.county,
        "country": event.venue.country,
        "latitude": float(event.venue.latitude),
        "longitude": float(event.venue.longitude),
        "organizer": event.organizer.name,
        "organizerVerified": event.organizer.verified,
        "priceFromMinor": min((tier.price_minor for tier in tiers), default=0),
        "priceAvailable": price_available,
        "currency": event.currency,
        "sellingFast": event.selling_fast,
        "featured": event.featured,
        "hotRank": event.hot_rank,
        "dateConfirmed": event.date_confirmed,
        "timeConfirmed": event.time_confirmed,
        "locationApproximate": event.venue.coordinates_are_approximate,
        "tags": [value for value in [event.category, event.mood, event.age_restriction] if value],
        "sourceName": radar_observation.source.name if radar_observation else "",
        "sourceUrl": (radar_observation.ticket_url or radar_observation.source_url) if radar_observation else "",
        "isExternalListing": bool(radar_observation),
        "ticketTiers": [
            {
                "id": str(tier.id),
                "name": tier.name,
                "priceMinor": tier.price_minor,
                "currency": tier.currency,
                "remaining": tier.remaining,
                "description": tier.description,
            }
            for tier in tiers
        ],
    }


def _published_events():
    return (
        Event.objects.filter(status=Event.Status.PUBLISHED)
        .select_related("venue", "organizer")
        .prefetch_related(Prefetch("ticket_tiers", queryset=TicketTier.objects.order_by("price_minor")))
        .prefetch_related("radar_observations__source")
    )


@require_GET
def health(request):
    return JsonResponse({"status": "ok", "service": "lets-go-event-django-admin"})


@require_GET
def event_list(request):
    queryset = _published_events()
    category = request.GET.get("category", "").strip()
    city = request.GET.get("city", "").strip()
    county = request.GET.get("county", "").strip()
    if category:
        queryset = queryset.filter(category__iexact=category)
    if city:
        queryset = queryset.filter(venue__city__iexact=city)
    if county:
        queryset = queryset.filter(venue__county__iexact=county)
    items = [_serialize_event(request, event) for event in queryset[:200]]
    return JsonResponse({"count": len(items), "items": items})


@require_GET
def event_detail(request, slug: str):
    try:
        event = _published_events().get(slug=slug)
    except Event.DoesNotExist as exc:
        raise Http404("Published event not found") from exc
    return JsonResponse(_serialize_event(request, event))


@csrf_exempt
@require_POST
def create_event_draft(request):
    """Creates an unpublished event; public visibility still requires an admin publish action."""
    payload = _payload(request)
    if not isinstance(payload, dict):
        return _error("Invalid JSON request body.")
    required = ("title", "summary", "category", "startsAt", "venue", "city", "address", "ticketName", "ticketPrice", "quantity")
    if any(not str(payload.get(field, "")).strip() for field in required):
        return _error("Please complete every required event field.")
    try:
        starts_at = timezone.datetime.fromisoformat(str(payload["startsAt"]).replace("Z", "+00:00"))
        if timezone.is_naive(starts_at):
            starts_at = timezone.make_aware(starts_at, timezone.get_current_timezone())
        price_minor = int(float(payload["ticketPrice"]) * 100)
        quantity = int(payload["quantity"])
        if price_minor < 0 or not 1 <= quantity <= 100000:
            raise ValueError
    except (TypeError, ValueError):
        return _error("Enter a valid start date, ticket price and inventory quantity.")
    base_slug = slugify(str(payload["title"]))[:150] or "event"
    slug = base_slug
    suffix = 2
    while Event.objects.filter(slug=slug).exists():
        slug = f"{base_slug[:150-len(str(suffix))-1]}-{suffix}"
        suffix += 1
    organizer, _ = Organizer.objects.get_or_create(
        slug="self-service-organizers", defaults={"name": "Self-service organizers", "verified": False},
    )
    venue_slug = slugify(f"{payload['venue']}-{payload['city']}")[:160] or "venue"
    venue, _ = Venue.objects.get_or_create(
        slug=venue_slug,
        defaults={
            "name": str(payload["venue"]).strip(), "address": str(payload["address"]).strip(),
            "city": str(payload["city"]).strip(), "county": str(payload.get("county") or payload["city"]).strip(),
            "area": str(payload.get("area") or "").strip(), "latitude": "0", "longitude": "0",
            "coordinates_are_approximate": True,
        },
    )
    event = Event.objects.create(
        organizer=organizer, venue=venue, title=str(payload["title"]).strip(), slug=slug,
        summary=str(payload["summary"]).strip()[:240], description=str(payload["summary"]).strip(),
        category=str(payload["category"]), status=Event.Status.DRAFT, starts_at=starts_at,
        ends_at=starts_at + timedelta(hours=4), external_image_url="https://images.unsplash.com/photo-1492684223066-81342ee5ff30",
    )
    TicketTier.objects.create(event=event, name=str(payload["ticketName"]).strip(), price_minor=price_minor, capacity=quantity)
    return JsonResponse({"id": str(event.id), "slug": event.slug, "status": event.status, "message": "Draft created. Publish it from Django Admin after review."}, status=201)


@csrf_exempt
@require_POST
def create_location_suggestion(request):
    payload = _payload(request)
    required = ("county", "area", "eventType", "timing")
    if not isinstance(payload, dict) or any(not str(payload.get(field, "")).strip() for field in required):
        return _error("Please choose a county, area, event type and preferred time.")
    suggestion = LocationSuggestion.objects.create(
        county=str(payload["county"]).strip()[:100],
        area=str(payload["area"]).strip()[:100],
        event_type=str(payload["eventType"]).strip()[:100],
        timing=str(payload["timing"]).strip()[:50],
        note=str(payload.get("note", "")).strip()[:2000],
    )
    return JsonResponse({"id": suggestion.pk, "message": "Suggestion saved for the Let's Go team."}, status=201)


@csrf_exempt
@require_POST
def create_order(request):
    payload = _payload(request)
    if not isinstance(payload, dict) or not isinstance(payload.get("items"), list):
        return _error("A ticket selection is required.")
    phone_number = _normalize_mpesa_phone(payload.get("phoneNumber"))
    if not phone_number:
        return _error("Enter a valid Kenyan M-PESA number, such as 0712345678.")
    requested = {}
    for item in payload["items"]:
        try:
            tier_id, quantity = str(item["tierId"]), int(item["quantity"])
        except (KeyError, TypeError, ValueError):
            return _error("Ticket selection is invalid.")
        if not 1 <= quantity <= 6:
            return _error("You can reserve between 1 and 6 tickets per tier.")
        requested[tier_id] = requested.get(tier_id, 0) + quantity
    if not requested:
        return _error("Choose at least one ticket.")
    with transaction.atomic():
        tiers = list(TicketTier.objects.select_for_update().select_related("event").filter(id__in=requested))
        if len(tiers) != len(requested):
            return _error("One or more ticket tiers are unavailable.", 404)
        events = {tier.event_id for tier in tiers}
        if len(events) != 1 or any(tier.event.status != Event.Status.PUBLISHED for tier in tiers):
            return _error("Tickets can only be reserved for one published event.")
        for tier in tiers:
            if tier.remaining < requested[str(tier.id)]:
                return _error(f"{tier.name} no longer has enough availability.", 409)
        order = Order.objects.create(event=tiers[0].event, total_minor=sum(tier.price_minor * requested[str(tier.id)] for tier in tiers), currency=tiers[0].currency, reservation_expires_at=timezone.now() + timedelta(minutes=10), phone_number=phone_number)
        for tier in tiers:
            quantity = requested[str(tier.id)]
            TicketTier.objects.filter(pk=tier.pk).update(reserved_count=F("reserved_count") + quantity)
            OrderItem.objects.create(order=order, tier=tier, quantity=quantity, unit_price_minor=tier.price_minor)
    try:
        mpesa_response = initiate_stk_push(order, phone_number)
    except DarajaError as error:
        with transaction.atomic():
            failed_order = Order.objects.select_for_update().get(pk=order.pk)
            if failed_order.status == Order.Status.RESERVED:
                for item in failed_order.items.select_related("tier"):
                    TicketTier.objects.filter(pk=item.tier_id).update(reserved_count=F("reserved_count") - item.quantity)
                failed_order.status = Order.Status.CANCELLED
                failed_order.payment_status = Order.PaymentStatus.FAILED
                failed_order.payment_result_desc = str(error)[:255]
                failed_order.save(update_fields=["status", "payment_status", "payment_result_desc", "updated_at"])
        return _error(str(error), 503)

    order.payment_status = Order.PaymentStatus.PENDING
    order.checkout_request_id = str(mpesa_response["CheckoutRequestID"])
    order.merchant_request_id = str(mpesa_response.get("MerchantRequestID", ""))[:100]
    order.payment_result_desc = str(mpesa_response.get("CustomerMessage") or "STK Push sent. Enter your M-PESA PIN to complete payment.")[:255]
    order.save(update_fields=["payment_status", "checkout_request_id", "merchant_request_id", "payment_result_desc", "updated_at"])
    return JsonResponse({"reference": order.reference, "status": order.status, "paymentStatus": order.payment_status, "expiresAt": order.reservation_expires_at.isoformat(), "totalMinor": order.total_minor, "currency": order.currency, "message": order.payment_result_desc}, status=201)


@csrf_exempt
@require_POST
def mpesa_callback(request):
    payload = _payload(request)
    body = payload.get("Body") if isinstance(payload, dict) else None
    callback = body.get("stkCallback") if isinstance(body, dict) else None
    if not isinstance(callback, dict) or not callback.get("CheckoutRequestID"):
        return _error("Invalid M-PESA callback.")

    checkout_id = str(callback["CheckoutRequestID"])
    try:
        result_code = int(callback.get("ResultCode"))
    except (TypeError, ValueError):
        return _error("Invalid M-PESA callback result.")

    candidate = Order.objects.filter(checkout_request_id=checkout_id).only(
        "merchant_request_id", "status", "payment_status",
    ).first()
    if candidate is None:
        return _error("Order not found for this M-PESA checkout.", 404)
    if candidate.merchant_request_id and str(callback.get("MerchantRequestID", "")) != candidate.merchant_request_id:
        return _error("M-PESA request identifiers do not match.", 400)
    if candidate.status != Order.Status.RESERVED or candidate.payment_status != Order.PaymentStatus.PENDING:
        return JsonResponse({"ResultCode": 0, "ResultDesc": "Callback already processed."})

    if result_code == 0:
        try:
            daraja_status = query_stk_push(checkout_id)
        except DarajaError as error:
            return _error(str(error), 503)
        if str(daraja_status.get("ResponseCode", "")) != "0" or str(daraja_status.get("ResultCode", "")) != "0":
            return _error("Daraja has not confirmed this payment yet.", 409)

    with transaction.atomic():
        try:
            order = Order.objects.select_for_update().prefetch_related("items").get(checkout_request_id=checkout_id)
        except Order.DoesNotExist:
            return _error("Order not found for this M-PESA checkout.", 404)
        if order.status != Order.Status.RESERVED or order.payment_status != Order.PaymentStatus.PENDING:
            return JsonResponse({"ResultCode": 0, "ResultDesc": "Callback already processed."})
        if order.merchant_request_id and str(callback.get("MerchantRequestID", "")) != order.merchant_request_id:
            return _error("M-PESA request identifiers do not match.", 400)

        if result_code == 0:
            metadata = callback.get("CallbackMetadata", {}).get("Item", [])
            values = {str(item.get("Name")): item.get("Value") for item in metadata if isinstance(item, dict)}
            try:
                paid_minor = int((Decimal(str(values["Amount"])) * 100).quantize(Decimal("1")))
            except (KeyError, InvalidOperation, TypeError, ValueError):
                return _error("Successful M-PESA callback is missing its amount.")
            callback_phone = _normalize_mpesa_phone(values.get("PhoneNumber"))
            receipt = str(values.get("MpesaReceiptNumber") or "").strip()
            if paid_minor != order.total_minor or callback_phone != order.phone_number or not receipt:
                return _error("M-PESA payment details did not match the reserved order.")

            for item in order.items.select_related("tier"):
                TicketTier.objects.filter(pk=item.tier_id).update(
                    reserved_count=F("reserved_count") - item.quantity,
                    sold_count=F("sold_count") + item.quantity,
                )
                Ticket.objects.bulk_create([Ticket(order=order, tier=item.tier) for _ in range(item.quantity)])
            order.status = Order.Status.PAID
            order.payment_status = Order.PaymentStatus.COMPLETED
            order.mpesa_receipt_number = receipt[:32]
        else:
            for item in order.items.all():
                TicketTier.objects.filter(pk=item.tier_id).update(reserved_count=F("reserved_count") - item.quantity)
            order.status = Order.Status.CANCELLED
            order.payment_status = Order.PaymentStatus.FAILED

        order.payment_result_desc = str(callback.get("ResultDesc", ""))[:255]
        order.save(update_fields=["status", "payment_status", "mpesa_receipt_number", "payment_result_desc", "updated_at"])
    return JsonResponse({"ResultCode": 0, "ResultDesc": "Callback processed."})


@require_GET
def order_status(request, reference: str):
    try:
        order = Order.objects.get(reference=reference)
    except Order.DoesNotExist as exc:
        raise Http404("Order not found") from exc
    return JsonResponse({
        "reference": order.reference,
        "status": order.status,
        "paymentStatus": order.payment_status,
        "message": order.payment_result_desc,
        "receipt": order.mpesa_receipt_number,
    })


@csrf_exempt
@require_POST
def scan_ticket(request):
    payload = _payload(request)
    code = str(payload.get("code", "")).strip().upper() if isinstance(payload, dict) else ""
    if not code:
        return _error("Enter or scan a ticket code.")
    with transaction.atomic():
        try:
            ticket = Ticket.objects.select_for_update().select_related("order__event", "tier").get(code=code)
        except Ticket.DoesNotExist:
            return _error("Ticket not found.", 404)
        if ticket.order.status != Order.Status.PAID:
            return _error("This ticket has not been paid for.", 409)
        if ticket.checked_in_at:
            return JsonResponse({"valid": False, "error": "Ticket has already been checked in.", "checkedInAt": ticket.checked_in_at.isoformat()}, status=409)
        ticket.checked_in_at = timezone.now()
        ticket.save(update_fields=["checked_in_at"])
    return JsonResponse({"valid": True, "ticket": ticket.code, "event": ticket.order.event.title, "tier": ticket.tier.name, "checkedInAt": ticket.checked_in_at.isoformat()})

