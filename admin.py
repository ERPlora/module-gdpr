from django.contrib import admin

from .models import ConsentRecord, DataRequest

@admin.register(ConsentRecord)
class ConsentRecordAdmin(admin.ModelAdmin):
    list_display = ['subject_name', 'subject_email', 'purpose', 'consented', 'consent_date']
    readonly_fields = ['id', 'hub_id', 'created_at', 'updated_at']
    ordering = ['-created_at']


@admin.register(DataRequest)
class DataRequestAdmin(admin.ModelAdmin):
    list_display = ['subject_name', 'subject_email', 'request_type', 'status', 'completed_at']
    readonly_fields = ['id', 'hub_id', 'created_at', 'updated_at']
    ordering = ['-created_at']

