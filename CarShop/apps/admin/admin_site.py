from django.contrib import admin
from django.views.decorators.cache import never_cache
from django.contrib.admin.apps import AdminConfig
import json

class CustomAdminConfig(AdminConfig):
    default_site = 'apps.admin.CustomAdminSite'


class CustomAdminSite(admin.AdminSite):
    def index(self, request, extra_context=None):
        from apps.shop.models import Category

        categories = Category.objects.all()
        categories_counts = {}

        categories_len = len(categories)

        for index, category in enumerate(categories):
            category_count = len(category.product_set.all())
            categories_counts[category.name] = category_count

        categories_counts = json.dumps(categories_counts)

        return super().index(request, extra_context={'categories_counts': categories_counts})
