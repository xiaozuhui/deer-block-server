from django.contrib import admin

from apps.bussiness.models import Category, Tag


class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "label", "user")
    list_filter = ('user')
    list_per_page = 40


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "label", 'level')
    list_per_page = 40
