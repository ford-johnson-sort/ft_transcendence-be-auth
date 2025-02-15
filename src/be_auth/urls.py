from django.contrib import admin
from django.urls import include, path

# TODO 2FA using email
urlpatterns = [
    path("auth/admin/", admin.site.urls),
    path('auth/oauth/', include('oauth.urls')),
    path('auth/mfa/', include('mfa.urls'))
]
