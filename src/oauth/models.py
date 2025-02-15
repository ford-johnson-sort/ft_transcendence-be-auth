from django.db import models

from be_auth_model.models import User


class UserOauthInformation(models.Model):
    """user oauth token table"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
    token_access = models.CharField(max_length=64)
    token_refresh = models.CharField(max_length=64)
    token_expire = models.DateTimeField()
