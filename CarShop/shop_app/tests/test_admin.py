import datetime

from django.contrib.admin import AdminSite
from django.test import TestCase
from shop_app.admin import BuyAdmin
from shop_app.models import Buy
from django.test import RequestFactory
from django.contrib.messages.storage.fallback import FallbackStorage


class MockSuperUser:
    def has_perm(self, perm):
        return True


request_factory = RequestFactory()
request = request_factory.get('/admin')
request.user = MockSuperUser()

request.session = 'session'
messages = FallbackStorage(request)
request._messages = messages


class TestBuyAdmin(TestCase):
    def setUp(self):
        self.test_obj = Buy.objects.create(
            pk=1,
            date=datetime.date(2021, 3, 24),
            product_name="Hot wheel",
            count=2
        )

        site = AdminSite()
        self.test_admin = BuyAdmin(Buy, site)

    def test_delete_model(self):
        self.test_admin.delete_model(request, self.test_obj)

        deleted = Buy.objects.filter(pk=1).first()
        self.assertEqual(deleted, None)

    def test_has_change_permission(self):
        res = self.test_admin.has_change_permission(request)
        self.assertFalse(res)
