from django.contrib import admin

from apps.users import model2
from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "phone_number")


@admin.register(model2.UserProfile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', "gender", "birthday")
