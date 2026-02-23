from django.urls import path
from . import views

app_name = 'gdpr'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('consents/', views.consents, name='consents'),
    path('requests/', views.requests, name='requests'),
    path('settings/', views.settings, name='settings'),
]
