"""base models for be_auth project"""
from django.db import models


class User(models.Model):
    """main user table"""
    intra = models.CharField()
    name = models.CharField()
    email = models.EmailField()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self) -> str:
        return self.intra

# TODO: design database schema
