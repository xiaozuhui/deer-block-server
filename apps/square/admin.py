from django.contrib import admin

from apps.square import models


@admin.register(models.Issues)
class IssuesAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "publisher", "status", "ip", "is_delete")
    list_filter = ('publisher', 'status', 'created_at')
    list_per_page = 40
    ordering = ('publisher', 'created_at',)


@admin.register(models.Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'issues', 'reply', 'publisher', 'is_delete')
    list_filter = ('publisher', 'issues__title',)
    list_per_page = 20
