from django.contrib import admin
from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth.models import Group as DjangoGroup

from .models import User


class UserAdmin(admin.ModelAdmin):
    fields = ["intra", "email"]


# register models
admin.site.register(User, UserAdmin)

# unregister Django auth models (not used)
admin.site.unregister(DjangoUser)
admin.site.unregister(DjangoGroup)
