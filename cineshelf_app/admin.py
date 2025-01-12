from django.contrib import admin
from .models  import Movie

# admin.site.register(Movie)

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'active')
    search_fields = ('name',)
    list_filter = ('active',)

