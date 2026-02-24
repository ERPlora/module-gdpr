"""Tests for gdpr models."""
import pytest
from django.utils import timezone

from gdpr.models import ConsentRecord, DataRequest


@pytest.mark.django_db
class TestConsentRecord:
    """ConsentRecord model tests."""

    def test_create(self, consent_record):
        """Test ConsentRecord creation."""
        assert consent_record.pk is not None
        assert consent_record.is_deleted is False

    def test_soft_delete(self, consent_record):
        """Test soft delete."""
        pk = consent_record.pk
        consent_record.is_deleted = True
        consent_record.deleted_at = timezone.now()
        consent_record.save()
        assert not ConsentRecord.objects.filter(pk=pk).exists()
        assert ConsentRecord.all_objects.filter(pk=pk).exists()

    def test_queryset_excludes_deleted(self, hub_id, consent_record):
        """Test default queryset excludes deleted."""
        consent_record.is_deleted = True
        consent_record.deleted_at = timezone.now()
        consent_record.save()
        assert ConsentRecord.objects.filter(hub_id=hub_id).count() == 0


@pytest.mark.django_db
class TestDataRequest:
    """DataRequest model tests."""

    def test_create(self, data_request):
        """Test DataRequest creation."""
        assert data_request.pk is not None
        assert data_request.is_deleted is False

    def test_soft_delete(self, data_request):
        """Test soft delete."""
        pk = data_request.pk
        data_request.is_deleted = True
        data_request.deleted_at = timezone.now()
        data_request.save()
        assert not DataRequest.objects.filter(pk=pk).exists()
        assert DataRequest.all_objects.filter(pk=pk).exists()

    def test_queryset_excludes_deleted(self, hub_id, data_request):
        """Test default queryset excludes deleted."""
        data_request.is_deleted = True
        data_request.deleted_at = timezone.now()
        data_request.save()
        assert DataRequest.objects.filter(hub_id=hub_id).count() == 0


