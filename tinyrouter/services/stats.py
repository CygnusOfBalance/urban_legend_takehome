from django.db.models import Count

from tinyrouter.models import Click, Link


def get_link_stats(slug: str) -> dict:
    if not Link.objects.filter(slug=slug).exists():
        raise Link.DoesNotExist

    clicks = Click.objects.filter(slug=slug, is_bot=False)

    total_clicks = clicks.count()
    unique_ips = (
        clicks.exclude(ip_address__isnull=True)
        .values("ip_address")
        .distinct()
        .count()
    )

    by_country: dict[str, int] = {}
    for row in clicks.values("country").annotate(count=Count("id")):
        key = row["country"] if row["country"] else "unknown"
        by_country[key] = row["count"]

    return {
        "slug": slug,
        "total_clicks": total_clicks,
        "unique_ips": unique_ips,
        "by_country": by_country,
    }
