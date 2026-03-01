"""AI tools for the GDPR module."""
from assistant.tools import AssistantTool, register_tool


@register_tool
class ListConsentRecords(AssistantTool):
    name = "list_consent_records"
    description = "List GDPR consent records."
    module_id = "gdpr"
    required_permission = "gdpr.view_consentrecord"
    parameters = {
        "type": "object",
        "properties": {"purpose": {"type": "string"}, "consented": {"type": "boolean"}, "limit": {"type": "integer"}},
        "required": [],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from gdpr.models import ConsentRecord
        qs = ConsentRecord.objects.all()
        if args.get('purpose'):
            qs = qs.filter(purpose__icontains=args['purpose'])
        if 'consented' in args:
            qs = qs.filter(consented=args['consented'])
        limit = args.get('limit', 20)
        return {"records": [{"id": str(r.id), "subject_name": r.subject_name, "subject_email": r.subject_email, "purpose": r.purpose, "consented": r.consented, "consent_date": r.consent_date.isoformat() if r.consent_date else None} for r in qs[:limit]]}


@register_tool
class ListDataRequests(AssistantTool):
    name = "list_data_requests"
    description = "List GDPR data requests (access, erasure, portability, rectification)."
    module_id = "gdpr"
    required_permission = "gdpr.view_datarequest"
    parameters = {
        "type": "object",
        "properties": {"request_type": {"type": "string", "description": "access, erasure, portability, rectification"}, "status": {"type": "string"}},
        "required": [],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from gdpr.models import DataRequest
        qs = DataRequest.objects.all()
        if args.get('request_type'):
            qs = qs.filter(request_type=args['request_type'])
        if args.get('status'):
            qs = qs.filter(status=args['status'])
        return {"requests": [{"id": str(r.id), "subject_name": r.subject_name, "request_type": r.request_type, "status": r.status, "created_at": r.created_at.isoformat()} for r in qs.order_by('-created_at')]}


@register_tool
class CreateDataRequest(AssistantTool):
    name = "create_data_request"
    description = "Create a GDPR data request."
    module_id = "gdpr"
    required_permission = "gdpr.add_datarequest"
    requires_confirmation = True
    parameters = {
        "type": "object",
        "properties": {
            "subject_name": {"type": "string"}, "subject_email": {"type": "string"},
            "request_type": {"type": "string", "description": "access, erasure, portability, rectification"},
            "notes": {"type": "string"},
        },
        "required": ["subject_name", "subject_email", "request_type"],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from gdpr.models import DataRequest
        r = DataRequest.objects.create(subject_name=args['subject_name'], subject_email=args['subject_email'], request_type=args['request_type'], notes=args.get('notes', ''))
        return {"id": str(r.id), "created": True}
