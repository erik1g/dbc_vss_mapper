from django.contrib import admin
from .models import DBCData, DBCMessage, DBCSignal

@admin.register(DBCSignal)
class DBCSignalAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'message',
        'unit',
        'start_bit',
        'length',
        'byte_order',
        'is_signed',
        'choices'
    )
    search_fields = (
        'name', 
    )
    list_filter = (
        'byte_order', 'is_signed', 'unit'
    )
    readonly_fields = ()

@admin.register(DBCMessage)
class DBCMessageAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'frame_id', 'length', 'dbc_data'
    )
    search_fields = (
        'name', 'frame_id', 'dbc_data__title'
    )
    list_filter = (
        'length',
    )
    readonly_fields = ()

@admin.register(DBCData)
class DBCDataAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'uploaded_by', 'uploaded_at')
    search_fields = ('title', 'project__title', 'uploaded_by__username')
    list_filter = ('project', 'uploaded_by')
    readonly_fields = ('uploaded_at',)

    fieldsets = (
        (None, {
            'fields': ('project', 'data','title', 'uploaded_by', 'uploaded_at')
        }),
    )