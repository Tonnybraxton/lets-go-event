"""Small server-side client for Safaricom Daraja M-PESA Express (STK Push)."""

import base64
import ipaddress
import json
import os
import re
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

from django.utils import timezone


class DarajaError(Exception):
    pass


def _config() -> dict[str, str]:
    names = (
        "MPESA_CONSUMER_KEY",
        "MPESA_CONSUMER_SECRET",
        "MPESA_SHORTCODE",
        "MPESA_PASSKEY",
        "MPESA_CALLBACK_URL",
    )
    values = {name: os.getenv(name, "").strip() for name in names}
    missing = [name for name, value in values.items() if not value]
    if missing:
        raise DarajaError("Daraja is not configured. Missing: " + ", ".join(missing))

    environment = os.getenv("MPESA_ENV", "sandbox").strip().lower()
    if environment not in {"sandbox", "production"}:
        raise DarajaError("MPESA_ENV must be 'sandbox' or 'production'.")
    callback = urlsplit(values["MPESA_CALLBACK_URL"])
    if callback.scheme != "https" or not callback.netloc:
        raise DarajaError("MPESA_CALLBACK_URL must be a public HTTPS URL.")
    hostname = callback.hostname or ""
    if hostname == "localhost" or hostname.endswith(".localhost"):
        raise DarajaError("MPESA_CALLBACK_URL must use a public host, not localhost.")
    try:
        if not ipaddress.ip_address(hostname).is_global:
            raise DarajaError("MPESA_CALLBACK_URL must use a public HTTPS host.")
    except ValueError:
        pass
    if not re.fullmatch(r"\d{5,7}", values["MPESA_SHORTCODE"]):
        raise DarajaError("MPESA_SHORTCODE must contain 5 to 7 digits.")

    values["environment"] = environment
    values["base_url"] = (
        "https://sandbox.safaricom.co.ke" if environment == "sandbox" else "https://api.safaricom.co.ke"
    )
    values["party_b"] = os.getenv("MPESA_PARTY_B", values["MPESA_SHORTCODE"]).strip()
    values["transaction_type"] = os.getenv("MPESA_TRANSACTION_TYPE", "CustomerPayBillOnline").strip()
    if not re.fullmatch(r"\d{5,7}", values["party_b"]):
        raise DarajaError("MPESA_PARTY_B must contain 5 to 7 digits.")
    if values["transaction_type"] not in {"CustomerPayBillOnline", "CustomerBuyGoodsOnline"}:
        raise DarajaError("MPESA_TRANSACTION_TYPE is not a supported M-PESA Express transaction type.")
    return values


def _request_json(url: str, *, method: str = "GET", headers: dict | None = None, body: dict | None = None) -> dict:
    data = json.dumps(body).encode("utf-8") if body is not None else None
    request = Request(url, data=data, headers=headers or {}, method=method)
    try:
        with urlopen(request, timeout=20) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        try:
            payload = json.loads(error.read().decode("utf-8"))
            detail = payload.get("errorMessage") or payload.get("ResponseDescription") or "Daraja rejected the request."
        except (json.JSONDecodeError, AttributeError):
            detail = "Daraja rejected the request."
        raise DarajaError(str(detail)[:255]) from error
    except (URLError, TimeoutError, json.JSONDecodeError) as error:
        raise DarajaError("Could not reach Daraja. Check the service connection and try again.") from error
    if not isinstance(payload, dict):
        raise DarajaError("Daraja returned an unexpected response.")
    return payload


def initiate_stk_push(order, phone_number: str) -> dict:
    config = _config()
    if order.currency != "KES" or order.total_minor < 100 or order.total_minor % 100:
        raise DarajaError("M-PESA checkout requires a whole-number amount of at least KES 1.")

    credentials = base64.b64encode(
        f"{config['MPESA_CONSUMER_KEY']}:{config['MPESA_CONSUMER_SECRET']}".encode("utf-8")
    ).decode("ascii")
    token_payload = _request_json(
        f"{config['base_url']}/oauth/v1/generate?grant_type=client_credentials",
        headers={"Authorization": f"Basic {credentials}"},
    )
    access_token = token_payload.get("access_token")
    if not access_token:
        raise DarajaError("Daraja did not return an access token. Check the app credentials.")

    timestamp = timezone.localtime(timezone.now()).strftime("%Y%m%d%H%M%S")
    password = base64.b64encode(
        f"{config['MPESA_SHORTCODE']}{config['MPESA_PASSKEY']}{timestamp}".encode("utf-8")
    ).decode("ascii")
    payload = {
        "BusinessShortCode": config["MPESA_SHORTCODE"],
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": config["transaction_type"],
        "Amount": order.total_minor // 100,
        "PartyA": phone_number,
        "PartyB": config["party_b"],
        "PhoneNumber": phone_number,
        "CallBackURL": config["MPESA_CALLBACK_URL"],
        "AccountReference": order.reference[-12:],
        "TransactionDesc": "Event tickets",
    }
    response = _request_json(
        f"{config['base_url']}/mpesa/stkpush/v1/processrequest",
        method="POST",
        headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"},
        body=payload,
    )
    if str(response.get("ResponseCode", "")) != "0" or not response.get("CheckoutRequestID"):
        raise DarajaError(str(response.get("ResponseDescription") or "Daraja did not accept the STK Push.")[:255])
    return response


def query_stk_push(checkout_request_id: str) -> dict:
    """Confirm a success callback against Daraja before issuing tickets."""
    config = _config()
    credentials = base64.b64encode(
        f"{config['MPESA_CONSUMER_KEY']}:{config['MPESA_CONSUMER_SECRET']}".encode("utf-8")
    ).decode("ascii")
    token_payload = _request_json(
        f"{config['base_url']}/oauth/v1/generate?grant_type=client_credentials",
        headers={"Authorization": f"Basic {credentials}"},
    )
    access_token = token_payload.get("access_token")
    if not access_token:
        raise DarajaError("Daraja did not return an access token while verifying payment.")

    timestamp = timezone.localtime(timezone.now()).strftime("%Y%m%d%H%M%S")
    password = base64.b64encode(
        f"{config['MPESA_SHORTCODE']}{config['MPESA_PASSKEY']}{timestamp}".encode("utf-8")
    ).decode("ascii")
    return _request_json(
        f"{config['base_url']}/mpesa/stkpushquery/v1/query",
        method="POST",
        headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"},
        body={
            "BusinessShortCode": config["MPESA_SHORTCODE"],
            "Password": password,
            "Timestamp": timestamp,
            "CheckoutRequestID": checkout_request_id,
        },
    )

