from django.contrib import admin
from . import models


@admin.register(models.Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', ]
    list_display_links = ['title', ]
    exclude = ['slug', ]


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title',]
    list_filter = ['title',]
    exclude = ['slug', ]