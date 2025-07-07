from django.contrib import admin
from .models import VSSData, VSSSignal

@admin.register(VSSData)
class VSSDataAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'uploaded_by', 'uploaded_at')
    search_fields = ('title', 'project__title', 'uploaded_by__username')
    list_filter = ('project', 'uploaded_by')
    readonly_fields = ('uploaded_at',)

    fieldsets = (
        (None, {
            'fields': ('project', 'title', 'data', 'uploaded_by', 'uploaded_at')
        }),
    )

@admin.register(VSSSignal)
class VSSSignalAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'api_name', 'type', 'vss_data', 'parent_api_name',
        'unit', 'datatype'
    )
    search_fields = (
        'name', 'api_name', 'vss_data__title', 'parent_api_name', 'description'
    )
    list_filter = ('type', 'datatype', 'unit')
    readonly_fields = ()
    fieldsets = (
        (None, {
            'fields': (
                'vss_data',
                'name', 'api_name', 'type', 'datatype', 'unit', 'description',
                'api_id', 'api_uuid', 'parent_api_name', 'metadata'
            )
        }),
    )
