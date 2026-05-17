from django.urls import path

from tinyrouter.views.links import LinkCreateView
from tinyrouter.views.redirect import RedirectView
from tinyrouter.views.stats import LinkStatsView
from tinyrouter.views.stats_html import LinkStatsHtmlView

urlpatterns = [
    path("links", LinkCreateView.as_view(), name="link-create"),
    path("links/<slug>/stats", LinkStatsView.as_view(), name="link-stats"),
    path("links/<slug>", LinkStatsHtmlView.as_view(), name="link-stats-html"),
    path("r/<slug>", RedirectView.as_view(), name="redirect"),
]
