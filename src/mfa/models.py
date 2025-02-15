import uuid

from django.db import models

from be_auth_model.models import User


class User2FALogs(models.Model):
    """user 2fa information table"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    token = models.UUIDField(default=uuid.uuid4)
    login = models.DateTimeField(null=True, default=None)

    class Meta:
        verbose_name = "User 2FA Information"
        verbose_name_plural = "User 2FA Informations"

    def __str__(self) -> str:
        return f"{self.user} - logged in at {self.login}"
