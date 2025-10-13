from django.apps import AppConfig


class RotinasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rotinas'

    def ready(self):
        import rotinas.signals
