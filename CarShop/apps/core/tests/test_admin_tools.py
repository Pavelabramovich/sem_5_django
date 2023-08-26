from django.test import TestCase, RequestFactory
from django.contrib.messages.storage.fallback import FallbackStorage
from django.db import models
from django.contrib import admin

from apps.core.admin_tools import admin_override


class MockSuperUser:
    def has_perm(self, perm):
        return True


request_factory = RequestFactory()
request = request_factory.get('/admin')
request.user = MockSuperUser()

request.session = 'session'
messages = FallbackStorage(request)
request._messages = messages
