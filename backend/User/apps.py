from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'User'

    def ready(self):
        import User.signals  # Import signals.py here to ensure signal handlers are registered