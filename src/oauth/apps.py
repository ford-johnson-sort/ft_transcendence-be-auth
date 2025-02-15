from django.apps import AppConfig


# pylint: disable=C0115
class OauthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'oauth'
    verbose_name = 'Users - 42 OAuth'
