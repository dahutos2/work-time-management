from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class WorkTimeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "work_time"
    verbose_name = verbose_name_plural = _("勤務システム")
