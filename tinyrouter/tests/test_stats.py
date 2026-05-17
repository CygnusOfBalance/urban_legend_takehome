from django.test import Client, TestCase, override_settings

from tinyrouter.models import Click, Link


@override_settings(ALLOWED_HOSTS=["testserver", "localhost", "127.0.0.1"])
class LinkStatsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.link = Link.objects.create(
            destination_url="https://example.com",
            campaign_code="spring2026",
            creator_handle="@somebody",
            slug="abc123",
        )

    def test_stats_returns_correct_counts(self):
        Click.objects.create(
            link=self.link,
            slug=self.link.slug,
            ip_address="1.1.1.1",
            user_agent="Mozilla/5.0",
            query_params={},
            is_bot=False,
            country="US",
        )
        Click.objects.create(
            link=self.link,
            slug=self.link.slug,
            ip_address="1.1.1.1",
            user_agent="Mozilla/5.0",
            query_params={},
            is_bot=False,
            country="US",
        )
        Click.objects.create(
            link=self.link,
            slug=self.link.slug,
            ip_address="2.2.2.2",
            user_agent="Mozilla/5.0",
            query_params={},
            is_bot=False,
            country="CA",
        )
        Click.objects.create(
            link=self.link,
            slug=self.link.slug,
            ip_address="3.3.3.3",
            user_agent="Twitterbot/1.0",
            query_params={},
            is_bot=True,
            country="ZZ",
        )

        response = self.client.get(f"/links/{self.link.slug}/stats")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "slug": "abc123",
                "total_clicks": 3,
                "unique_ips": 2,
                "by_country": {"US": 2, "CA": 1},
            },
        )
