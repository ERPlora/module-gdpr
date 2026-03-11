"""
AI context for the GDPR module.
Loaded into the assistant system prompt when this module's tools are active.
"""

CONTEXT = """
## Module Knowledge: GDPR

### Models

**ConsentRecord** — tracks whether a data subject has given/withdrawn consent.
- `subject_name` (str): name of the person
- `subject_email` (email): contact email
- `purpose` (str, max 100): what the consent is for (e.g. "marketing", "analytics", "third_party_sharing")
- `consented` (bool): True = active consent, False = not consented or withdrawn
- `consent_date` (datetime, nullable): when consent was given
- `withdrawal_date` (datetime, nullable): when consent was withdrawn

**DataRequest** — tracks GDPR data subject requests (DSARs).
- `subject_name` (str): name of the requester
- `subject_email` (email): contact email
- `request_type` (choice): one of `access`, `erasure`, `portability`, `rectification`
- `status` (str, default "pending"): workflow state — typically: pending → in_progress → completed
- `completed_at` (datetime, nullable): when the request was fulfilled
- `notes` (text): internal handling notes

### Key flows

1. **Record consent**: create a ConsentRecord with purpose, subject info, consented=True, consent_date=now.
2. **Withdraw consent**: update ConsentRecord — set consented=False, withdrawal_date=now.
3. **Handle a DSAR**: create DataRequest with request_type and subject info, status="pending". Update status as it progresses. Set completed_at when done.
4. **Check active consents**: filter ConsentRecord by subject_email + purpose + consented=True.

### Request type choices
- `access` — Data Access (subject wants to know what data is held)
- `erasure` — Right to Erasure (right to be forgotten)
- `portability` — Data Portability (export data in machine-readable format)
- `rectification` — Rectification (correct inaccurate data)
"""
