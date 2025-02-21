from django.urls import path
from . import views

app_name = "mfa"
urlpatterns = [
    path('mail/<uuid:key>', views.email_2fa_challenge, name='email_2fa_challenge')
]
