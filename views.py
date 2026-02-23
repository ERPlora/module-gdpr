"""
GDPR & Privacy Module Views
"""
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from apps.accounts.decorators import login_required
from apps.core.htmx import htmx_view
from apps.modules_runtime.navigation import with_module_nav


@login_required
@with_module_nav('gdpr', 'dashboard')
@htmx_view('gdpr/pages/dashboard.html', 'gdpr/partials/dashboard_content.html')
def dashboard(request):
    """Dashboard view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('gdpr', 'consents')
@htmx_view('gdpr/pages/consents.html', 'gdpr/partials/consents_content.html')
def consents(request):
    """Consents view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('gdpr', 'requests')
@htmx_view('gdpr/pages/requests.html', 'gdpr/partials/requests_content.html')
def requests(request):
    """Requests view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('gdpr', 'settings')
@htmx_view('gdpr/pages/settings.html', 'gdpr/partials/settings_content.html')
def settings(request):
    """Settings view."""
    hub_id = request.session.get('hub_id')
    return {}

