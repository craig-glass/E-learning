from django.apps import AppConfig
from django.db.models.signals import post_save


class AccountsConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        from django.conf import settings
        from .models import set_default_groups
        post_save.connect(set_default_groups, sender=settings.AUTH_USER_MODEL)
