from django.conf import settings
from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from tinyrouter.models import Link
from tinyrouter.serializers import LinkCreateSerializer
from tinyrouter.services.slug import generate_unique_slug


class LinkCreateView(APIView):
    def post(self, request):
        serializer = LinkCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        for _ in range(10):
            try:
                slug = generate_unique_slug()
                link = Link.objects.create(slug=slug, **serializer.validated_data)
                break
            except IntegrityError:
                continue
        else:
            return Response(
                {"detail": "Could not allocate a unique slug."},
                status=status.HTTP_409_CONFLICT,
            )

        base_url = settings.APP_BASE_URL.rstrip("/")
        return Response(
            {"slug": link.slug, "short_url": f"{base_url}/r/{link.slug}"},
            status=status.HTTP_201_CREATED,
        )
