from django.contrib import admin
from .models import Janore, Kino, Komentari


@admin.register(Janore)
class JanoreAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(Kino)
class KinoAdmin(admin.ModelAdmin):
    list_display = ['name', 'year', 'country']
    list_filter = ['year', 'country', 'janore']
    search_fields = ['name', 'description']
    filter_horizontal = ['janore']


@admin.register(Komentari)
class KomentariAdmin(admin.ModelAdmin):
    list_display = ['name', 'kino', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'text', 'kino__name']
