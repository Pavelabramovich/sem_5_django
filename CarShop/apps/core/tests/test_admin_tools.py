from django.test import TestCase, RequestFactory
from django.contrib.messages.storage.fallback import FallbackStorage
from django.db import models
from django.contrib import admin
from django.contrib.admin import AdminSite

from apps.core.admin_tools import admin_override
from .models import Model


class MockSuperUser:
    def has_perm(self, perm):
        return True


request_factory = RequestFactory()
request = request_factory.get('/admin')
request.user = MockSuperUser()

request.session = 'session'
messages = FallbackStorage(request)
request._messages = messages


class TestAdminOverride(TestCase):
    def setUp(self):
        self.site = AdminSite()

        @admin.register(Model, site=self.site)
        class ModelAdmin(admin.ModelAdmin):
            pass

    def tearDown(self):
        self.site.unregister(Model)

    def test_no_models(self):
        with self.assertRaises(ValueError):
            @admin_override(site=self.site)
            class OtherModelAdmin(admin.ModelAdmin):
                pass

    def test_not_admin_site(self):
        with self.assertRaises(ValueError):
            @admin_override(Model, site=123)
            class OtherModelAdmin(admin.ModelAdmin):
                pass

    def test_not_admin_class(self):
        with self.assertRaises(ValueError):
            @admin_override(Model, site=self.site)
            class NotAdminClass:
                pass

    def test_normal(self):
        @admin_override(Model, site=self.site)
        class OtherModelAdmin(admin.ModelAdmin):
            pass

        current_model_admin = self.site._registry[Model]

        self.assertIsInstance(current_model_admin, OtherModelAdmin)


class TestFieldsetsInlineMixin(TestCase):
    pass


