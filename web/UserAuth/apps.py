from django.apps import AppConfig


class UserauthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'UserAuth'

    def ready(self):
        import UserAuth.signals
