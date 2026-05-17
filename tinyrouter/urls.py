from django.urls import path

from tinyrouter.views.links import LinkCreateView
from tinyrouter.views.redirect import RedirectView
from tinyrouter.views.stats import LinkStatsView

urlpatterns = [
    path("links", LinkCreateView.as_view(), name="link-create"),
    path("links/<slug>/stats", LinkStatsView.as_view(), name="link-stats"),
    path("r/<slug>", RedirectView.as_view(), name="redirect"),
]
