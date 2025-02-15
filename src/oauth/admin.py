from django.contrib import admin

from .models import UserOauthInformation


class UserOauthInformationAdmin(admin.ModelAdmin):
    """admin page view for OAuth information. only shows token expire date"""
    fields = ["user", "token_expire"]


admin.site.register(UserOauthInformation, UserOauthInformationAdmin)
