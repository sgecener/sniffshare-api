from django.apps import AppConfig


class SniffapiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sniffapi'

    def ready(self):
         import sniffapi.signals  # Import signals module