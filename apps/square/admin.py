from django.contrib import admin

from apps.square import models


@admin.register(models.Issues)
class IssuesAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "publisher", "status", "is_delete")
    list_filter = ('publisher', 'status', 'created_at')
    list_per_page = 40
    ordering = ('publisher', 'created_at',)


@admin.register(models.Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'issues', 'reply', 'publisher', 'is_delete')
    list_filter = ('publisher', 'issues__title',)
    list_per_page = 20


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('publisher', 'issues')
    list_per_page = 20


@admin.register(models.ThumbsUp)
class ThumbsUpAdmin(admin.ModelAdmin):
    list_display = ('publisher', 'issues')
    list_per_page = 20
