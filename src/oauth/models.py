from django.db import models


class User(models.Model):
    """basic user information table"""
    # postgresql supports unlimited VARCHAR
    intra = models.CharField()
    name = models.CharField()
    email = models.EmailField()

    token_access = models.CharField(max_length=64)
    token_refresh = models.CharField(max_length=64)
    token_expire = models.DateTimeField()


# TODO: design database schema
