from django.contrib.admin import ModelAdmin
from django.contrib.admin.sites import AdminSite
from django.contrib.admin.sites import site as default_site


def admin_override(*models, site=None):
    def _model_admin_wrapper(admin_class):
        if not models:
            raise ValueError("At least one model must be passed to override.")

        admin_site = site or default_site

        if not isinstance(admin_site, AdminSite):
            raise ValueError("site must subclass AdminSite")

        if not issubclass(admin_class, ModelAdmin):
            raise ValueError("Wrapped class must subclass ModelAdmin.")

        admin_site.unregister(models)
        admin_site.register(models, admin_class=admin_class)

        return admin_class

    return _model_admin_wrapper

