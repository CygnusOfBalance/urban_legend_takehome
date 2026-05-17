from django.test import Client, TestCase, override_settings

from tinyrouter.models import Click, Link


@override_settings(ALLOWED_HOSTS=["testserver", "localhost", "127.0.0.1"])
class BotRedirectSkipsClickTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.link = Link.objects.create(
            destination_url="https://example.com",
            campaign_code="spring2026",
            creator_handle="@somebody",
            slug="abc123",
        )

    def test_bot_user_agent_redirects_without_recording_click(self):
        response = self.client.get(
            "/r/abc123",
            HTTP_USER_AGENT="Twitterbot/1.0",
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Click.objects.count(), 0)
