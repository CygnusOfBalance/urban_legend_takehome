from django.http import Http404, HttpResponseRedirect
from django.views import View

from tinyrouter.bot_filter import is_bot
from tinyrouter.enrichment import enrich_click_async
from tinyrouter.models import Click, Link
from tinyrouter.services.dedup import is_duplicate_click
from tinyrouter.services.utm import append_query_params


def _client_ip(request) -> str | None:
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


class RedirectView(View):
    def get(self, request, slug):
        try:
            link = Link.objects.get(slug=slug)
        except Link.DoesNotExist as exc:
            raise Http404 from exc

        destination = append_query_params(link.destination_url, request.GET.dict())
        user_agent = request.META.get("HTTP_USER_AGENT")

        ip_address = _client_ip(request)
        if not is_bot(user_agent) and not is_duplicate_click(slug, ip_address):
            click = Click.objects.create(
                link=link,
                slug=slug,
                ip_address=ip_address,
                user_agent=user_agent or "",
                query_params=request.GET.dict(),
                is_bot=False,
            )
            enrich_click_async(click.id)

        return HttpResponseRedirect(destination)
