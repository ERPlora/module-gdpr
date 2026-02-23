from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class GdprConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gdpr'
    label = 'gdpr'
    verbose_name = _('GDPR & Privacy')

    def ready(self):
        pass
