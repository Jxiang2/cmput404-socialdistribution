from django.apps import AppConfig


class SdapisConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sdapis'

    def ready(self):
        import sdapis.signals
