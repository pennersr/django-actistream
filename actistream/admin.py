from django.contrib import admin

from .models import Activity, Notice


class NoticeAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display = (
        'activity',
        'user',
        'created_at',
        'read_at',
        'archived_at')
    raw_id_fields = (
        'user',
        'activity')
    list_filter = (
        'created_at',)


class ActivityAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display = (
        'type',
        'created_at')
    list_filter = (
        'created_at',)


admin.site.register(Notice, NoticeAdmin)
admin.site.register(Activity, ActivityAdmin)
