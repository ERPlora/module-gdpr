from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.base import HubBaseModel

REQ_TYPE = [
    ('access', _('Data Access')),
    ('erasure', _('Right to Erasure')),
    ('portability', _('Data Portability')),
    ('rectification', _('Rectification')),
]

class ConsentRecord(HubBaseModel):
    subject_name = models.CharField(max_length=255, verbose_name=_('Subject Name'))
    subject_email = models.EmailField(verbose_name=_('Subject Email'))
    purpose = models.CharField(max_length=100, verbose_name=_('Purpose'))
    consented = models.BooleanField(default=False, verbose_name=_('Consented'))
    consent_date = models.DateTimeField(null=True, blank=True, verbose_name=_('Consent Date'))
    withdrawal_date = models.DateTimeField(null=True, blank=True, verbose_name=_('Withdrawal Date'))

    class Meta(HubBaseModel.Meta):
        db_table = 'gdpr_consentrecord'

    def __str__(self):
        return str(self.id)


class DataRequest(HubBaseModel):
    subject_name = models.CharField(max_length=255, verbose_name=_('Subject Name'))
    subject_email = models.EmailField(verbose_name=_('Subject Email'))
    request_type = models.CharField(max_length=30, choices=REQ_TYPE, verbose_name=_('Request Type'))
    status = models.CharField(max_length=20, default='pending', verbose_name=_('Status'))
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Completed At'))
    notes = models.TextField(blank=True, verbose_name=_('Notes'))

    class Meta(HubBaseModel.Meta):
        db_table = 'gdpr_datarequest'

    def __str__(self):
        return str(self.id)

