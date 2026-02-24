from django.contrib import admin

from .models import ConsentRecord, DataRequest

@admin.register(ConsentRecord)
class ConsentRecordAdmin(admin.ModelAdmin):
    list_display = ['subject_name', 'subject_email', 'purpose', 'consented', 'consent_date', 'created_at']
    search_fields = ['subject_name', 'subject_email', 'purpose']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(DataRequest)
class DataRequestAdmin(admin.ModelAdmin):
    list_display = ['subject_name', 'subject_email', 'request_type', 'status', 'completed_at', 'created_at']
    search_fields = ['subject_name', 'subject_email', 'request_type', 'status']
    readonly_fields = ['created_at', 'updated_at']

