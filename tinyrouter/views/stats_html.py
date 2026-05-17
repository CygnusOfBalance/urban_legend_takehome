from django.http import Http404
from django.shortcuts import render
from django.views import View

from tinyrouter.models import Link
from tinyrouter.services.stats import get_link_stats


class LinkStatsHtmlView(View):
    def get(self, request, slug):
        try:
            link = Link.objects.get(slug=slug)
        except Link.DoesNotExist as exc:
            raise Http404 from exc

        return render(
            request,
            "tinyrouter/link_stats.html",
            {"link": link, "stats": get_link_stats(slug)},
        )
