"""base models for be_auth project"""
from django.db import models


class User(models.Model):
    """main user table"""
    intra = models.CharField()
    name = models.CharField()
    email = models.EmailField()


# TODO: design database schema
