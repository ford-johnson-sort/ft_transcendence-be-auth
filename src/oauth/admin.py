from django.contrib import admin

from .models import UserOauthInformation


class UserOauthInformationAdmin(admin.ModelAdmin):
    fields = ["user", "token_expire"]


admin.site.register(UserOauthInformation, UserOauthInformationAdmin)
