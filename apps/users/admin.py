from django.contrib import admin

from apps.users import model2, model_level
from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "phone_number")


@admin.register(model2.UserProfile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', "gender", "birthday")


@admin.register(model_level.Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ("id", "level_name", "level", "base_upgrade_exp", "is_default",)


@admin.register(model_level.LevelGroup)
class LevelGroupAdmin(admin.ModelAdmin):
    list_display = ("id", "min_level", "max_level", "is_default",)


@admin.register(model_level.UpgradeMethod)
class UpgradeMethodAdmin(admin.ModelAdmin):
    list_display = ("id", "upgrade_name", "base_exp_value", "is_default",)
