from django.apps import AppConfig


class BodegaappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bodegaApp'

    def ready(self):
        import bodegaApp.signals