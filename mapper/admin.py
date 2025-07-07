from django.contrib import admin

from django.contrib import admin
from .models import VssDbcMappingData

@admin.register(VssDbcMappingData)
class VssDbcMappingDataAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'created_by', 'created_at')
    search_fields = ('title', 'project__title')
    list_filter = ('project', 'created_by')
