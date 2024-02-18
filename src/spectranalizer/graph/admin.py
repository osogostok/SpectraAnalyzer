from django.contrib import admin

# Register your models here.
from .models import *

class SpectrAdmin(admin.ModelAdmin):
    list_display = ("id", "file_name")
    list_diaplay_links = ("id", "file_name")
    search_fields = ("file_name",)

admin.site.register(Spectr, SpectrAdmin)