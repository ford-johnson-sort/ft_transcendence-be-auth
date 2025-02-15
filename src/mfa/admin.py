from django.contrib import admin

from .models import User2FALogs


class User2FALogsAdmin(admin.ModelAdmin):
    """admin page view for 2FA login information"""
    fields = ["user", "login"]


admin.site.register(User2FALogs, User2FALogsAdmin)
