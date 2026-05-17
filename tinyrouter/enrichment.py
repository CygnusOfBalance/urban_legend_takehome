import logging
import threading
from typing import Any

import requests
from django.db import close_old_connections

from tinyrouter.models import Click

logger = logging.getLogger(__name__)

IP_API_BASE = "http://ip-api.com/json"
IP_API_FIELDS = "status,country,regionName,isp,as"
IP_API_TIMEOUT = 2


def fetch_geo(ip: str) -> dict[str, Any] | None:
    """Return country/region/asn/isp from ip-api.com, or None on failure."""
    if not ip:
        return None

    url = f"{IP_API_BASE}/{ip}"
    try:
        response = requests.get(
            url,
            params={"fields": IP_API_FIELDS},
            timeout=IP_API_TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()
    except (requests.RequestException, ValueError) as exc:
        logger.warning("ip-api lookup failed for %s: %s", ip, exc)
        return None

    if data.get("status") != "success":
        logger.warning(
            "ip-api non-success for %s: %s",
            ip,
            data.get("message", data),
        )
        return None

    return {
        "country": data.get("country") or None,
        "region": data.get("regionName") or None,
        "asn": data.get("as") or None,
        "isp": data.get("isp") or None,
    }


def apply_enrichment(click_id: int) -> None:
    """Fetch geo for a click's IP and persist enrichment fields."""
    try:
        click = Click.objects.get(pk=click_id)
    except Click.DoesNotExist:
        logger.warning("click %s not found for enrichment", click_id)
        return

    if not click.ip_address:
        return

    geo = fetch_geo(str(click.ip_address))
    if not geo:
        return

    Click.objects.filter(pk=click_id).update(**geo)


def enrich_click_async(click_id: int) -> None:
    """Enqueue ip-api enrichment on a background thread (does not block redirect)."""
    thread = threading.Thread(target=_run_enrichment, args=(click_id,), daemon=True)
    thread.start()


def _run_enrichment(click_id: int) -> None:
    close_old_connections()
    try:
        apply_enrichment(click_id)
    finally:
        close_old_connections()
