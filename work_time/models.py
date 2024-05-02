from django.db import models

# Create your models here.
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, UserManager
from django.urls import reverse_lazy
import datetime
from django.utils import timezone


class UserManager(UserManager):
    pass


class User(AbstractUser):
    email = models.EmailField("メールアドレス", unique=False, blank=True)
    full_name = models.CharField(
        "氏名",
        blank=True,
        max_length=255,
    )

    class Meta:
        verbose_name = verbose_name_plural = _("アカウント")

    def get_absolute_url(self):
        return reverse_lazy("/")

    def __str__(self):
        return str(self.full_name)


class WorkTime(models.Model):
    """スケジュール"""

    start_time = models.TimeField("開始時間", default=datetime.time(0, 0, 0))
    end_time = models.TimeField("終了時間", default=datetime.time(0, 0, 0))
    description = models.TextField("メモ", blank=True)
    date = models.DateField("日付")
    created_at = models.DateTimeField("作成日", default=timezone.now)
    name = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="related_user",
        verbose_name="ユーザー",
    )

    class Meta:
        verbose_name = verbose_name_plural = _("勤務時間")

    def __str__(self):
        return str(self.date)
