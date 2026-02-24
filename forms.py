from django import forms
from django.utils.translation import gettext_lazy as _

from .models import ConsentRecord, DataRequest

class ConsentRecordForm(forms.ModelForm):
    class Meta:
        model = ConsentRecord
        fields = ['subject_name', 'subject_email', 'purpose', 'consented', 'consent_date', 'withdrawal_date']
        widgets = {
            'subject_name': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'subject_email': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'email'}),
            'purpose': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'consented': forms.CheckboxInput(attrs={'class': 'toggle'}),
            'consent_date': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'datetime-local'}),
            'withdrawal_date': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'datetime-local'}),
        }

class DataRequestForm(forms.ModelForm):
    class Meta:
        model = DataRequest
        fields = ['subject_name', 'subject_email', 'request_type', 'status', 'completed_at', 'notes']
        widgets = {
            'subject_name': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'subject_email': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'email'}),
            'request_type': forms.Select(attrs={'class': 'select select-sm w-full'}),
            'status': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'completed_at': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'class': 'textarea textarea-sm w-full', 'rows': 3}),
        }

