from django.urls import path

from tinyrouter.views.links import LinkCreateView

urlpatterns = [
    path("links", LinkCreateView.as_view(), name="link-create"),
]
