from unittest.mock import patch

from django.test import Client, TestCase, override_settings

from tinyrouter.models import Click, Link


@override_settings(ALLOWED_HOSTS=["testserver", "localhost", "127.0.0.1"])
class RedirectRecordsClickTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.link = Link.objects.create(
            destination_url="https://example.com/landing",
            campaign_code="spring2026",
            creator_handle="@somebody",
            slug="abc123",
        )

    @patch("tinyrouter.views.redirect.enrich_click_async")
    def test_redirect_records_click(self, _mock_enrich):
        response = self.client.get(
            "/r/abc123?utm_source=email",
            HTTP_USER_AGENT="Mozilla/5.0",
            REMOTE_ADDR="203.0.113.10",
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("utm_source=email", response["Location"])

        self.assertEqual(Click.objects.count(), 1)
        click = Click.objects.get()
        self.assertEqual(click.slug, self.link.slug)
        self.assertEqual(click.ip_address, "203.0.113.10")
        self.assertEqual(click.query_params, {"utm_source": "email"})
        self.assertFalse(click.is_bot)
