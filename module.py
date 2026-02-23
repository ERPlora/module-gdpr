    from django.utils.translation import gettext_lazy as _

    MODULE_ID = 'gdpr'
    MODULE_NAME = _('GDPR & Privacy')
    MODULE_VERSION = '1.0.0'
    MODULE_ICON = 'lock-closed-outline'
    MODULE_DESCRIPTION = _('GDPR consent management, data subject requests and privacy compliance')
    MODULE_AUTHOR = 'ERPlora'
    MODULE_CATEGORY = 'compliance'

    MENU = {
        'label': _('GDPR & Privacy'),
        'icon': 'lock-closed-outline',
        'order': 82,
    }

    NAVIGATION = [
        {'label': _('Dashboard'), 'icon': 'speedometer-outline', 'id': 'dashboard'},
{'label': _('Consents'), 'icon': 'lock-closed-outline', 'id': 'consents'},
{'label': _('Requests'), 'icon': 'person-outline', 'id': 'requests'},
{'label': _('Settings'), 'icon': 'settings-outline', 'id': 'settings'},
    ]

    DEPENDENCIES = []

    PERMISSIONS = [
        'gdpr.view_consentrecord',
'gdpr.manage_consent',
'gdpr.view_datarequest',
'gdpr.process_datarequest',
'gdpr.manage_settings',
    ]
