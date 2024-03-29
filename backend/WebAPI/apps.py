from django.apps import AppConfig


class WebapiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "WebAPI"

    def ready(self):
        import WebAPI.signals