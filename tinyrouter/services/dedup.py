from datetime import timedelta

from django.utils import timezone

from tinyrouter.models import Click

DEDUP_WINDOW = timedelta(seconds=5)


def is_duplicate_click(slug: str, ip_address: str | None) -> bool:
    if not ip_address:
        return False

    cutoff = timezone.now() - DEDUP_WINDOW
    return Click.objects.filter(
        slug=slug,
        ip_address=ip_address,
        clicked_at__gte=cutoff,
    ).exists()
