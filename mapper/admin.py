from django.contrib import admin

from django.contrib import admin
from .models import VssDbcMappingData, VssDbcMappingEntry

@admin.register(VssDbcMappingData)
class VssDbcMappingDataAdmin(admin.ModelAdmin):
    list_display = ['title', 'project', 'created_by', 'created_at']
    search_fields = ['title', 'project__title', 'created_by__username']
    list_filter = ['project', 'created_by']
    readonly_fields = ['created_at']

@admin.register(VssDbcMappingEntry)
class VssDbcMappingEntryAdmin(admin.ModelAdmin):
    list_display = ['mapping_data', 'vss_signal', 'dbc_signal']
    search_fields = [
        'mapping_data__title',
        'vss_signal__path',
        'dbc_signal__name'
    ]
    list_filter = ['mapping_data']
    autocomplete_fields = ['mapping_data', 'vss_signal', 'dbc_signal']