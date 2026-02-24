"""
GDPR & Privacy Module Views
"""
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404, render as django_render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

from apps.accounts.decorators import login_required
from apps.core.htmx import htmx_view
from apps.core.services import export_to_csv, export_to_excel
from apps.modules_runtime.navigation import with_module_nav

from .models import ConsentRecord, DataRequest

PER_PAGE_CHOICES = [10, 25, 50, 100]


# ======================================================================
# Dashboard
# ======================================================================

@login_required
@with_module_nav('gdpr', 'dashboard')
@htmx_view('gdpr/pages/index.html', 'gdpr/partials/dashboard_content.html')
def dashboard(request):
    hub_id = request.session.get('hub_id')
    return {
        'total_consent_records': ConsentRecord.objects.filter(hub_id=hub_id, is_deleted=False).count(),
        'total_data_requests': DataRequest.objects.filter(hub_id=hub_id, is_deleted=False).count(),
    }


# ======================================================================
# ConsentRecord
# ======================================================================

CONSENT_RECORD_SORT_FIELDS = {
    'consented': 'consented',
    'subject_name': 'subject_name',
    'subject_email': 'subject_email',
    'purpose': 'purpose',
    'consent_date': 'consent_date',
    'withdrawal_date': 'withdrawal_date',
    'created_at': 'created_at',
}

def _build_consent_records_context(hub_id, per_page=10):
    qs = ConsentRecord.objects.filter(hub_id=hub_id, is_deleted=False).order_by('consented')
    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(1)
    return {
        'consent_records': page_obj,
        'page_obj': page_obj,
        'search_query': '',
        'sort_field': 'consented',
        'sort_dir': 'asc',
        'current_view': 'table',
        'per_page': per_page,
    }

def _render_consent_records_list(request, hub_id, per_page=10):
    ctx = _build_consent_records_context(hub_id, per_page)
    return django_render(request, 'gdpr/partials/consent_records_list.html', ctx)

@login_required
@with_module_nav('gdpr', 'consents')
@htmx_view('gdpr/pages/consent_records.html', 'gdpr/partials/consent_records_content.html')
def consent_records_list(request):
    hub_id = request.session.get('hub_id')
    search_query = request.GET.get('q', '').strip()
    sort_field = request.GET.get('sort', 'consented')
    sort_dir = request.GET.get('dir', 'asc')
    page_number = request.GET.get('page', 1)
    current_view = request.GET.get('view', 'table')
    per_page = int(request.GET.get('per_page', 10))
    if per_page not in PER_PAGE_CHOICES:
        per_page = 10

    qs = ConsentRecord.objects.filter(hub_id=hub_id, is_deleted=False)

    if search_query:
        qs = qs.filter(Q(subject_name__icontains=search_query) | Q(subject_email__icontains=search_query) | Q(purpose__icontains=search_query))

    order_by = CONSENT_RECORD_SORT_FIELDS.get(sort_field, 'consented')
    if sort_dir == 'desc':
        order_by = f'-{order_by}'
    qs = qs.order_by(order_by)

    export_format = request.GET.get('export')
    if export_format in ('csv', 'excel'):
        fields = ['consented', 'subject_name', 'subject_email', 'purpose', 'consent_date', 'withdrawal_date']
        headers = ['Consented', 'Subject Name', 'Subject Email', 'Purpose', 'Consent Date', 'Withdrawal Date']
        if export_format == 'csv':
            return export_to_csv(qs, fields=fields, headers=headers, filename='consent_records.csv')
        return export_to_excel(qs, fields=fields, headers=headers, filename='consent_records.xlsx')

    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(page_number)

    if request.htmx and request.htmx.target == 'datatable-body':
        return django_render(request, 'gdpr/partials/consent_records_list.html', {
            'consent_records': page_obj, 'page_obj': page_obj,
            'search_query': search_query, 'sort_field': sort_field,
            'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
        })

    return {
        'consent_records': page_obj, 'page_obj': page_obj,
        'search_query': search_query, 'sort_field': sort_field,
        'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
    }

@login_required
def consent_record_add(request):
    hub_id = request.session.get('hub_id')
    if request.method == 'POST':
        subject_name = request.POST.get('subject_name', '').strip()
        subject_email = request.POST.get('subject_email', '').strip()
        purpose = request.POST.get('purpose', '').strip()
        consented = request.POST.get('consented') == 'on'
        consent_date = request.POST.get('consent_date') or None
        withdrawal_date = request.POST.get('withdrawal_date') or None
        obj = ConsentRecord(hub_id=hub_id)
        obj.subject_name = subject_name
        obj.subject_email = subject_email
        obj.purpose = purpose
        obj.consented = consented
        obj.consent_date = consent_date
        obj.withdrawal_date = withdrawal_date
        obj.save()
        return _render_consent_records_list(request, hub_id)
    return django_render(request, 'gdpr/partials/panel_consent_record_add.html', {})

@login_required
def consent_record_edit(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(ConsentRecord, pk=pk, hub_id=hub_id, is_deleted=False)
    if request.method == 'POST':
        obj.subject_name = request.POST.get('subject_name', '').strip()
        obj.subject_email = request.POST.get('subject_email', '').strip()
        obj.purpose = request.POST.get('purpose', '').strip()
        obj.consented = request.POST.get('consented') == 'on'
        obj.consent_date = request.POST.get('consent_date') or None
        obj.withdrawal_date = request.POST.get('withdrawal_date') or None
        obj.save()
        return _render_consent_records_list(request, hub_id)
    return django_render(request, 'gdpr/partials/panel_consent_record_edit.html', {'obj': obj})

@login_required
@require_POST
def consent_record_delete(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(ConsentRecord, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_deleted = True
    obj.deleted_at = timezone.now()
    obj.save(update_fields=['is_deleted', 'deleted_at', 'updated_at'])
    return _render_consent_records_list(request, hub_id)

@login_required
@require_POST
def consent_records_bulk_action(request):
    hub_id = request.session.get('hub_id')
    ids = [i.strip() for i in request.POST.get('ids', '').split(',') if i.strip()]
    action = request.POST.get('action', '')
    qs = ConsentRecord.objects.filter(hub_id=hub_id, is_deleted=False, id__in=ids)
    if action == 'delete':
        qs.update(is_deleted=True, deleted_at=timezone.now())
    return _render_consent_records_list(request, hub_id)


# ======================================================================
# DataRequest
# ======================================================================

DATA_REQUEST_SORT_FIELDS = {
    'request_type': 'request_type',
    'status': 'status',
    'subject_name': 'subject_name',
    'subject_email': 'subject_email',
    'completed_at': 'completed_at',
    'notes': 'notes',
    'created_at': 'created_at',
}

def _build_data_requests_context(hub_id, per_page=10):
    qs = DataRequest.objects.filter(hub_id=hub_id, is_deleted=False).order_by('request_type')
    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(1)
    return {
        'data_requests': page_obj,
        'page_obj': page_obj,
        'search_query': '',
        'sort_field': 'request_type',
        'sort_dir': 'asc',
        'current_view': 'table',
        'per_page': per_page,
    }

def _render_data_requests_list(request, hub_id, per_page=10):
    ctx = _build_data_requests_context(hub_id, per_page)
    return django_render(request, 'gdpr/partials/data_requests_list.html', ctx)

@login_required
@with_module_nav('gdpr', 'consents')
@htmx_view('gdpr/pages/data_requests.html', 'gdpr/partials/data_requests_content.html')
def data_requests_list(request):
    hub_id = request.session.get('hub_id')
    search_query = request.GET.get('q', '').strip()
    sort_field = request.GET.get('sort', 'request_type')
    sort_dir = request.GET.get('dir', 'asc')
    page_number = request.GET.get('page', 1)
    current_view = request.GET.get('view', 'table')
    per_page = int(request.GET.get('per_page', 10))
    if per_page not in PER_PAGE_CHOICES:
        per_page = 10

    qs = DataRequest.objects.filter(hub_id=hub_id, is_deleted=False)

    if search_query:
        qs = qs.filter(Q(subject_name__icontains=search_query) | Q(subject_email__icontains=search_query) | Q(request_type__icontains=search_query) | Q(status__icontains=search_query))

    order_by = DATA_REQUEST_SORT_FIELDS.get(sort_field, 'request_type')
    if sort_dir == 'desc':
        order_by = f'-{order_by}'
    qs = qs.order_by(order_by)

    export_format = request.GET.get('export')
    if export_format in ('csv', 'excel'):
        fields = ['request_type', 'status', 'subject_name', 'subject_email', 'completed_at', 'notes']
        headers = ['Request Type', 'Status', 'Subject Name', 'Subject Email', 'Completed At', 'Notes']
        if export_format == 'csv':
            return export_to_csv(qs, fields=fields, headers=headers, filename='data_requests.csv')
        return export_to_excel(qs, fields=fields, headers=headers, filename='data_requests.xlsx')

    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(page_number)

    if request.htmx and request.htmx.target == 'datatable-body':
        return django_render(request, 'gdpr/partials/data_requests_list.html', {
            'data_requests': page_obj, 'page_obj': page_obj,
            'search_query': search_query, 'sort_field': sort_field,
            'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
        })

    return {
        'data_requests': page_obj, 'page_obj': page_obj,
        'search_query': search_query, 'sort_field': sort_field,
        'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
    }

@login_required
def data_request_add(request):
    hub_id = request.session.get('hub_id')
    if request.method == 'POST':
        subject_name = request.POST.get('subject_name', '').strip()
        subject_email = request.POST.get('subject_email', '').strip()
        request_type = request.POST.get('request_type', '').strip()
        status = request.POST.get('status', '').strip()
        completed_at = request.POST.get('completed_at') or None
        notes = request.POST.get('notes', '').strip()
        obj = DataRequest(hub_id=hub_id)
        obj.subject_name = subject_name
        obj.subject_email = subject_email
        obj.request_type = request_type
        obj.status = status
        obj.completed_at = completed_at
        obj.notes = notes
        obj.save()
        return _render_data_requests_list(request, hub_id)
    return django_render(request, 'gdpr/partials/panel_data_request_add.html', {})

@login_required
def data_request_edit(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(DataRequest, pk=pk, hub_id=hub_id, is_deleted=False)
    if request.method == 'POST':
        obj.subject_name = request.POST.get('subject_name', '').strip()
        obj.subject_email = request.POST.get('subject_email', '').strip()
        obj.request_type = request.POST.get('request_type', '').strip()
        obj.status = request.POST.get('status', '').strip()
        obj.completed_at = request.POST.get('completed_at') or None
        obj.notes = request.POST.get('notes', '').strip()
        obj.save()
        return _render_data_requests_list(request, hub_id)
    return django_render(request, 'gdpr/partials/panel_data_request_edit.html', {'obj': obj})

@login_required
@require_POST
def data_request_delete(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(DataRequest, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_deleted = True
    obj.deleted_at = timezone.now()
    obj.save(update_fields=['is_deleted', 'deleted_at', 'updated_at'])
    return _render_data_requests_list(request, hub_id)

@login_required
@require_POST
def data_requests_bulk_action(request):
    hub_id = request.session.get('hub_id')
    ids = [i.strip() for i in request.POST.get('ids', '').split(',') if i.strip()]
    action = request.POST.get('action', '')
    qs = DataRequest.objects.filter(hub_id=hub_id, is_deleted=False, id__in=ids)
    if action == 'delete':
        qs.update(is_deleted=True, deleted_at=timezone.now())
    return _render_data_requests_list(request, hub_id)


@login_required
@with_module_nav('gdpr', 'settings')
@htmx_view('gdpr/pages/settings.html', 'gdpr/partials/settings_content.html')
def settings_view(request):
    return {}

