from rest_framework import serializers


class LinkCreateSerializer(serializers.Serializer):
    destination_url = serializers.URLField(max_length=2048)
    campaign_code = serializers.CharField(max_length=255)
    creator_handle = serializers.CharField(max_length=255)
