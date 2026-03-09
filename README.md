# GDPR & Privacy

## Overview

| Property | Value |
|----------|-------|
| **Module ID** | `gdpr` |
| **Version** | `1.0.0` |
| **Icon** | `lock-closed-outline` |
| **Dependencies** | None |

## Models

### `ConsentRecord`

ConsentRecord(id, hub_id, created_at, updated_at, created_by, updated_by, is_deleted, deleted_at, subject_name, subject_email, purpose, consented, consent_date, withdrawal_date)

| Field | Type | Details |
|-------|------|---------|
| `subject_name` | CharField | max_length=255 |
| `subject_email` | EmailField | max_length=254 |
| `purpose` | CharField | max_length=100 |
| `consented` | BooleanField |  |
| `consent_date` | DateTimeField | optional |
| `withdrawal_date` | DateTimeField | optional |

### `DataRequest`

DataRequest(id, hub_id, created_at, updated_at, created_by, updated_by, is_deleted, deleted_at, subject_name, subject_email, request_type, status, completed_at, notes)

| Field | Type | Details |
|-------|------|---------|
| `subject_name` | CharField | max_length=255 |
| `subject_email` | EmailField | max_length=254 |
| `request_type` | CharField | max_length=30, choices: access, erasure, portability, rectification |
| `status` | CharField | max_length=20 |
| `completed_at` | DateTimeField | optional |
| `notes` | TextField | optional |

## URL Endpoints

Base path: `/m/gdpr/`

| Path | Name | Method |
|------|------|--------|
| `(root)` | `dashboard` | GET |
| `consents/` | `consents` | GET |
| `requests/` | `requests` | GET |
| `consent_records/` | `consent_records_list` | GET |
| `consent_records/add/` | `consent_record_add` | GET/POST |
| `consent_records/<uuid:pk>/edit/` | `consent_record_edit` | GET |
| `consent_records/<uuid:pk>/delete/` | `consent_record_delete` | GET/POST |
| `consent_records/bulk/` | `consent_records_bulk_action` | GET/POST |
| `data_requests/` | `data_requests_list` | GET |
| `data_requests/add/` | `data_request_add` | GET/POST |
| `data_requests/<uuid:pk>/edit/` | `data_request_edit` | GET |
| `data_requests/<uuid:pk>/delete/` | `data_request_delete` | GET/POST |
| `data_requests/bulk/` | `data_requests_bulk_action` | GET/POST |
| `settings/` | `settings` | GET |

## Permissions

| Permission | Description |
|------------|-------------|
| `gdpr.view_consentrecord` | View Consentrecord |
| `gdpr.manage_consent` | Manage Consent |
| `gdpr.view_datarequest` | View Datarequest |
| `gdpr.process_datarequest` | Process Datarequest |
| `gdpr.manage_settings` | Manage Settings |

**Role assignments:**

- **admin**: All permissions
- **manager**: `manage_consent`, `process_datarequest`, `view_consentrecord`, `view_datarequest`
- **employee**: `view_consentrecord`, `view_datarequest`

## Navigation

| View | Icon | ID | Fullpage |
|------|------|----|----------|
| Dashboard | `speedometer-outline` | `dashboard` | No |
| Consents | `lock-closed-outline` | `consents` | No |
| Requests | `person-outline` | `requests` | No |
| Settings | `settings-outline` | `settings` | No |

## AI Tools

Tools available for the AI assistant:

### `list_consent_records`

List GDPR consent records.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `purpose` | string | No |  |
| `consented` | boolean | No |  |
| `limit` | integer | No |  |

### `list_data_requests`

List GDPR data requests (access, erasure, portability, rectification).

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `request_type` | string | No | access, erasure, portability, rectification |
| `status` | string | No |  |

### `create_data_request`

Create a GDPR data request.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `subject_name` | string | Yes |  |
| `subject_email` | string | Yes |  |
| `request_type` | string | Yes | access, erasure, portability, rectification |
| `notes` | string | No |  |

## File Structure

```
README.md
__init__.py
admin.py
ai_tools.py
apps.py
forms.py
locale/
  en/
    LC_MESSAGES/
      django.po
  es/
    LC_MESSAGES/
      django.po
migrations/
  0001_initial.py
  __init__.py
models.py
module.py
static/
  gdpr/
    css/
    js/
  icons/
    icon.svg
templates/
  gdpr/
    pages/
      consent_record_add.html
      consent_record_edit.html
      consent_records.html
      consents.html
      dashboard.html
      data_request_add.html
      data_request_edit.html
      data_requests.html
      index.html
      requests.html
      settings.html
    partials/
      consent_record_add_content.html
      consent_record_edit_content.html
      consent_records_content.html
      consent_records_list.html
      consents_content.html
      dashboard_content.html
      data_request_add_content.html
      data_request_edit_content.html
      data_requests_content.html
      data_requests_list.html
      panel_consent_record_add.html
      panel_consent_record_edit.html
      panel_data_request_add.html
      panel_data_request_edit.html
      requests_content.html
      settings_content.html
tests/
  __init__.py
  conftest.py
  test_models.py
  test_views.py
urls.py
views.py
```
