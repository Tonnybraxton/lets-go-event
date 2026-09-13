import ipaddress
import socket
from urllib.parse import urlsplit, urlunsplit

from django.core.exceptions import ValidationError


TRACKING_PARAMETERS = {"utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content"}


def validate_public_url(url: str, *, resolve_dns: bool = False) -> str:
    parsed = urlsplit(url.strip())
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValidationError("Radar sources must use a public HTTP or HTTPS URL.")
    host = parsed.hostname.rstrip(".").lower()
    if host in {"localhost", "localhost.localdomain"} or host.endswith(".local"):
        raise ValidationError("Local and private hosts are not valid Radar sources.")
    addresses: set[str] = set()
    try:
        addresses.add(str(ipaddress.ip_address(host)))
    except ValueError:
        if resolve_dns:
            try:
                addresses.update(item[4][0] for item in socket.getaddrinfo(host, None))
            except socket.gaierror as exc:
                raise ValidationError("The source hostname could not be resolved.") from exc
    for address in addresses:
        value = ipaddress.ip_address(address)
        if not value.is_global:
            raise ValidationError("Radar cannot connect to private, loopback, or reserved networks.")
    return urlunsplit((parsed.scheme, parsed.netloc, parsed.path or "/", parsed.query, ""))
