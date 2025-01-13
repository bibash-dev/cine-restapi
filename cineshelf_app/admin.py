from django.contrib import admin
from .models import StreamPlatform, MediaStream


@admin.register(StreamPlatform)
class StreamPlatformAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "website_url")
    search_fields = ("name",)


@admin.register(MediaStream)
class MediaStreamAdmin(admin.ModelAdmin):
    list_display = ("title", "summary", "is_active", "created_at")
    search_fields = ("title",)
    list_filter = ("is_active",)
    ordering = ("-created_at",)

