from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from tinyrouter.models import Link
from tinyrouter.services.stats import get_link_stats


class LinkStatsView(APIView):
    def get(self, request, slug):
        if not Link.objects.filter(slug=slug).exists():
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(get_link_stats(slug))
