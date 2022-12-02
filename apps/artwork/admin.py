from django.contrib import admin

from apps.artwork.models import Art, Author


@admin.register(Art)
class ArtAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "is_original", "uploader", "is_uploader_has",)
    list_filter = ('title', "author", "uploader", "is_original",)
    list_per_page = 40


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "birthday", "contact", "related_user",)
    list_per_page = 40
