from django.contrib import admin
from django.urls import include, path

# TODO 2FA using email
urlpatterns = [
    path('auth/oauth/', include('oauth.urls')),
    path('auth/mfa/', include('mfa.urls'))
]
