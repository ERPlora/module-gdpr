# GDPR & Privacy Module

GDPR consent management, data subject requests, and privacy compliance.

## Features

- Record and manage consent records for data subjects with purpose tracking
- Track consent and withdrawal dates for audit compliance
- Process data subject requests: data access, right to erasure, data portability, and rectification
- Track request status and completion dates
- Maintain subject contact details (name, email) for all records
- Add notes to data requests for internal documentation
- Dashboard with overview of consent status and pending requests

## Installation

This module is installed automatically via the ERPlora Marketplace.

## Configuration

Access settings via: **Menu > GDPR & Privacy > Settings**

## Usage

Access via: **Menu > GDPR & Privacy**

### Views

| View | URL | Description |
|------|-----|-------------|
| Dashboard | `/m/gdpr/dashboard/` | Overview of consent records and data request status |
| Consents | `/m/gdpr/consents/` | View and manage consent records |
| Requests | `/m/gdpr/requests/` | Process and track data subject requests |
| Settings | `/m/gdpr/settings/` | Configure GDPR module settings |

## Models

| Model | Description |
|-------|-------------|
| `ConsentRecord` | Consent record with subject details, purpose, consent status, and consent/withdrawal dates |
| `DataRequest` | Data subject request with type (access, erasure, portability, rectification), status, and completion tracking |

## Permissions

| Permission | Description |
|------------|-------------|
| `gdpr.view_consentrecord` | View consent records |
| `gdpr.manage_consent` | Create, edit, and manage consent records |
| `gdpr.view_datarequest` | View data subject requests |
| `gdpr.process_datarequest` | Process and complete data subject requests |
| `gdpr.manage_settings` | Manage GDPR module settings |

## License

MIT

## Author

ERPlora Team - support@erplora.com
