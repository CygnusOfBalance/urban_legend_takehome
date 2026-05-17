from django.db import models


class Link(models.Model):
    destination_url = models.URLField(max_length=2048)
    campaign_code = models.CharField(max_length=255)
    creator_handle = models.CharField(max_length=255)
    slug = models.CharField(max_length=32, unique=True, db_index=True)

    def __str__(self):
        return self.slug


class Click(models.Model):
    link = models.ForeignKey(Link, on_delete=models.CASCADE, related_name="clicks")
    slug = models.CharField(max_length=32, db_index=True)
    clicked_at = models.DateTimeField(auto_now_add=True, db_index=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    query_params = models.JSONField()
    is_bot = models.BooleanField(default=False)
    country = models.CharField(max_length=64, null=True, blank=True)
    region = models.CharField(max_length=128, null=True, blank=True)
    asn = models.CharField(max_length=255, null=True, blank=True)
    isp = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ["-clicked_at"]

    def __str__(self):
        return f"{self.slug} @ {self.clicked_at}"
