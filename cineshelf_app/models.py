from django.db import models


class StreamPlatform(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=150)
    website_url = models.URLField(max_length=100)

    def __str__(self):
        return self.name


class MediaStream(models.Model):
    title = models.CharField(max_length=50)
    summary = models.TextField(max_length=200)
    platform = models.ForeignKey(
        StreamPlatform, on_delete=models.CASCADE, related_name="media_streams"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
