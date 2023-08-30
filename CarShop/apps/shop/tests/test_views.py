from django.test import Client
from apps.shop.views import (
    home,
)

from django.test import TestCase


class TestHome(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_url(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
