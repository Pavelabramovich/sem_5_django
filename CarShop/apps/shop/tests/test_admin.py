import datetime

from django.test import override_settings
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.contrib.messages.storage.fallback import FallbackStorage

import config.settings as settings
from apps.core.test_tools import AssertNestedSequencesEqualsMixin
from apps.shop.admin import (
    ProductAdmin,
    BuyAdmin,
    UserProfileAdmin
)
from apps.shop.models import (
    Product,
    Buy,
    Profile,
    Category,
    Provider
)


class MockSuperUser:
    def has_perm(self, perm):
        return True


request_factory = RequestFactory()
request = request_factory.get('/admin')
request.user = MockSuperUser()

request.session = 'session'
messages = FallbackStorage(request)
request._messages = messages


@override_settings(MEDIA_ROOT=settings.TEST_MEDIA_ROOT)
class TestProductAdmin(TestCase):
    def setUp(self):
        name = 'Expensive wipers'
        category = Category.objects.create(name='Cleaners')
        price = 100

        Provider.objects.create(
            id=1,
            username='Vova',
            password='password_123'),
        Provider.objects.create(
            id=2,
            username='Vasya',
            password='psswrd923'),
        Provider.objects.create(
            id=3,
            username='Vlad',
            password='15_06_2017')

        Profile.objects.create(
            id=1,
            user=User.objects.get(id=1),
            phone='+375 (29) 501-20-09',
            address="Smoky Lane 58, Smoglin"),
        Profile.objects.create(
            id=2,
            user=User.objects.get(id=2),
            phone='+375 (29) 039-28-11',
            address="Low avenue 37, Tromburg"),
        Profile.objects.create(
            id=3,
            user=User.objects.get(id=3),
            phone='+375 (29) 984-02-53',
            address="Quiet allay 8, Mandau"),

        self.test_obj = Product.objects.create(
            name=name,
            category=category,
            price=price)

        for i in range(1, 4):
            self.test_obj.providers.add(i)

        site = AdminSite()
        self.test_admin = ProductAdmin(Product, site)

    def test_get_providers_as_link(self):
        expected_res = """<a href="/admin/auth/user/?id__in=1%2C2%2C3">Vova, Vasya, Vlad</a>"""

        res = self.test_admin.get_providers_as_link(self.test_obj)

        self.assertEqual(res, expected_res)

    def tearDown(self):
        Profile.objects.get(id=1).delete()
        Profile.objects.get(id=2).delete()
        Profile.objects.get(id=3).delete()


class TestBuyAdmin(AssertNestedSequencesEqualsMixin, TestCase):
    def setUp(self):
        self.test_obj = Buy.objects.create(
            id=1,
            date=datetime.date(2021, 3, 24),
            product_name="Hot wheel",
            count=2
        )

        site = AdminSite()
        self.test_admin = BuyAdmin(Buy, site)

    def test_get_search_results_normal(self):
        search_term = "24 March 2021"

        expected_res = Buy.objects.filter(id=1), False
        res = self.test_admin.get_search_results(request, Buy.objects.all(), search_term)

        self.assertNestedSequencesEquals(res, expected_res)

    def test_has_change_permission(self):
        res = self.test_admin.has_change_permission(request)
        self.assertFalse(res)
