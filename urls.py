from django.urls import path
from . import views

app_name = 'gdpr'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # ConsentRecord
    path('consent_records/', views.consent_records_list, name='consent_records_list'),
    path('consent_records/add/', views.consent_record_add, name='consent_record_add'),
    path('consent_records/<uuid:pk>/edit/', views.consent_record_edit, name='consent_record_edit'),
    path('consent_records/<uuid:pk>/delete/', views.consent_record_delete, name='consent_record_delete'),
    path('consent_records/bulk/', views.consent_records_bulk_action, name='consent_records_bulk_action'),

    # DataRequest
    path('data_requests/', views.data_requests_list, name='data_requests_list'),
    path('data_requests/add/', views.data_request_add, name='data_request_add'),
    path('data_requests/<uuid:pk>/edit/', views.data_request_edit, name='data_request_edit'),
    path('data_requests/<uuid:pk>/delete/', views.data_request_delete, name='data_request_delete'),
    path('data_requests/bulk/', views.data_requests_bulk_action, name='data_requests_bulk_action'),

    # Settings
    path('settings/', views.settings_view, name='settings'),
]
