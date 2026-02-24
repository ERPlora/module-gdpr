"""Tests for gdpr views."""
import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestDashboard:
    """Dashboard view tests."""

    def test_dashboard_loads(self, auth_client):
        """Test dashboard page loads."""
        url = reverse('gdpr:dashboard')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_dashboard_htmx(self, auth_client):
        """Test dashboard HTMX partial."""
        url = reverse('gdpr:dashboard')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_dashboard_requires_auth(self, client):
        """Test dashboard requires authentication."""
        url = reverse('gdpr:dashboard')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestConsentRecordViews:
    """ConsentRecord view tests."""

    def test_list_loads(self, auth_client):
        """Test list view loads."""
        url = reverse('gdpr:consent_records_list')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_list_htmx(self, auth_client):
        """Test list HTMX partial."""
        url = reverse('gdpr:consent_records_list')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_list_search(self, auth_client):
        """Test list search."""
        url = reverse('gdpr:consent_records_list')
        response = auth_client.get(url, {'q': 'test'})
        assert response.status_code == 200

    def test_list_sort(self, auth_client):
        """Test list sorting."""
        url = reverse('gdpr:consent_records_list')
        response = auth_client.get(url, {'sort': 'created_at', 'dir': 'desc'})
        assert response.status_code == 200

    def test_export_csv(self, auth_client):
        """Test CSV export."""
        url = reverse('gdpr:consent_records_list')
        response = auth_client.get(url, {'export': 'csv'})
        assert response.status_code == 200
        assert 'text/csv' in response['Content-Type']

    def test_export_excel(self, auth_client):
        """Test Excel export."""
        url = reverse('gdpr:consent_records_list')
        response = auth_client.get(url, {'export': 'excel'})
        assert response.status_code == 200

    def test_add_form_loads(self, auth_client):
        """Test add form loads."""
        url = reverse('gdpr:consent_record_add')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_add_post(self, auth_client):
        """Test creating via POST."""
        url = reverse('gdpr:consent_record_add')
        data = {
            'subject_name': 'New Subject Name',
            'subject_email': 'test@example.com',
            'purpose': 'New Purpose',
            'consented': 'on',
            'consent_date': '2025-01-15T10:00',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_edit_form_loads(self, auth_client, consent_record):
        """Test edit form loads."""
        url = reverse('gdpr:consent_record_edit', args=[consent_record.pk])
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_edit_post(self, auth_client, consent_record):
        """Test editing via POST."""
        url = reverse('gdpr:consent_record_edit', args=[consent_record.pk])
        data = {
            'subject_name': 'Updated Subject Name',
            'subject_email': 'test@example.com',
            'purpose': 'Updated Purpose',
            'consented': '',
            'consent_date': '2025-01-15T10:00',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_delete(self, auth_client, consent_record):
        """Test soft delete via POST."""
        url = reverse('gdpr:consent_record_delete', args=[consent_record.pk])
        response = auth_client.post(url)
        assert response.status_code == 200
        consent_record.refresh_from_db()
        assert consent_record.is_deleted is True

    def test_bulk_delete(self, auth_client, consent_record):
        """Test bulk delete."""
        url = reverse('gdpr:consent_records_bulk_action')
        response = auth_client.post(url, {'ids': str(consent_record.pk), 'action': 'delete'})
        assert response.status_code == 200
        consent_record.refresh_from_db()
        assert consent_record.is_deleted is True

    def test_list_requires_auth(self, client):
        """Test list requires authentication."""
        url = reverse('gdpr:consent_records_list')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestDataRequestViews:
    """DataRequest view tests."""

    def test_list_loads(self, auth_client):
        """Test list view loads."""
        url = reverse('gdpr:data_requests_list')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_list_htmx(self, auth_client):
        """Test list HTMX partial."""
        url = reverse('gdpr:data_requests_list')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_list_search(self, auth_client):
        """Test list search."""
        url = reverse('gdpr:data_requests_list')
        response = auth_client.get(url, {'q': 'test'})
        assert response.status_code == 200

    def test_list_sort(self, auth_client):
        """Test list sorting."""
        url = reverse('gdpr:data_requests_list')
        response = auth_client.get(url, {'sort': 'created_at', 'dir': 'desc'})
        assert response.status_code == 200

    def test_export_csv(self, auth_client):
        """Test CSV export."""
        url = reverse('gdpr:data_requests_list')
        response = auth_client.get(url, {'export': 'csv'})
        assert response.status_code == 200
        assert 'text/csv' in response['Content-Type']

    def test_export_excel(self, auth_client):
        """Test Excel export."""
        url = reverse('gdpr:data_requests_list')
        response = auth_client.get(url, {'export': 'excel'})
        assert response.status_code == 200

    def test_add_form_loads(self, auth_client):
        """Test add form loads."""
        url = reverse('gdpr:data_request_add')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_add_post(self, auth_client):
        """Test creating via POST."""
        url = reverse('gdpr:data_request_add')
        data = {
            'subject_name': 'New Subject Name',
            'subject_email': 'test@example.com',
            'request_type': 'New Request Type',
            'status': 'New Status',
            'completed_at': '2025-01-15T10:00',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_edit_form_loads(self, auth_client, data_request):
        """Test edit form loads."""
        url = reverse('gdpr:data_request_edit', args=[data_request.pk])
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_edit_post(self, auth_client, data_request):
        """Test editing via POST."""
        url = reverse('gdpr:data_request_edit', args=[data_request.pk])
        data = {
            'subject_name': 'Updated Subject Name',
            'subject_email': 'test@example.com',
            'request_type': 'Updated Request Type',
            'status': 'Updated Status',
            'completed_at': '2025-01-15T10:00',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_delete(self, auth_client, data_request):
        """Test soft delete via POST."""
        url = reverse('gdpr:data_request_delete', args=[data_request.pk])
        response = auth_client.post(url)
        assert response.status_code == 200
        data_request.refresh_from_db()
        assert data_request.is_deleted is True

    def test_bulk_delete(self, auth_client, data_request):
        """Test bulk delete."""
        url = reverse('gdpr:data_requests_bulk_action')
        response = auth_client.post(url, {'ids': str(data_request.pk), 'action': 'delete'})
        assert response.status_code == 200
        data_request.refresh_from_db()
        assert data_request.is_deleted is True

    def test_list_requires_auth(self, client):
        """Test list requires authentication."""
        url = reverse('gdpr:data_requests_list')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestSettings:
    """Settings view tests."""

    def test_settings_loads(self, auth_client):
        """Test settings page loads."""
        url = reverse('gdpr:settings')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_settings_requires_auth(self, client):
        """Test settings requires authentication."""
        url = reverse('gdpr:settings')
        response = client.get(url)
        assert response.status_code == 302

