from django.contrib import admin
import django.contrib.auth.models as DjangoAuthModel

from .models import User


class UserAdmin(admin.ModelAdmin):
    """admin page view for managing user"""
    fields = ["intra", "email"]


# register models
admin.site.register(User, UserAdmin)

# unregister Django auth models (not used)
admin.site.unregister(DjangoAuthModel.User)
admin.site.unregister(DjangoAuthModel.Group)
