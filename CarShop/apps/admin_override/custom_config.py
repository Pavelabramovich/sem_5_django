from django.contrib import admin
from django.contrib.admin.apps import AdminConfig


from .views import CustomViewsAdminSite


class CustomAdminConfig(AdminConfig):
    default_site = 'apps.admin_override.custom_config.CustomAdminSite'


overrides = (
    CustomViewsAdminSite,
)

CustomAdminSite = type('CustomAdminSite', (*overrides, admin.AdminSite), {})
