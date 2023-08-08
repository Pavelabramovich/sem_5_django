from django.apps import AppConfig


class TestAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop_app'
    verbose_name = 'Car shop app'

    def ready(self):
        from . import signals
