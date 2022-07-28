from django.contrib import admin

from apps.bussiness.models import Category, Tag, Message


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "label", "user")
    list_filter = ('user',)
    list_per_page = 40


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "label", 'level')
    list_per_page = 40


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "source_type", "from_user", "to_user", "has_consumed")
    list_per_page = 20
