from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

APP_LABEL = 'fias'


class FIASConfig(AppConfig):
    name = APP_LABEL
    verbose_name = _('FIAS')
