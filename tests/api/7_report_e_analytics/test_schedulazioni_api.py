import pytest
from support.api_helpers import assert_status, assert_unauthorized


class TestSchedulazioniAPI:
    """
    Test API per il modulo Report & Analytics > Schedulazioni
    """

    def test_get_schedules_status_200(self, api_context):
        response = api_context.get("/api/reports/schedules")
        assert_status(response, 200)

    def test_get_ftp_connections_status_200(self, api_context):
        response = api_context.get("/api/ftp/connections")
        assert_status(response, 200)

    def test_post_create_schedule_status_200(self, api_context):
        payload = {
            "name": "Schedulazione Test API Automatico",
            "templateId": "tpl_1773914923215",
            "recipients": ["destinatario1@example.com", "destinatario2@example.com"],
            "delivery": [
                {
                    "type": "email",
                    "to": ["destinatario1@example.com", "destinatario2@example.com"]
                }
            ],
            "cronExpression": "0 8 * * 1",
            "format": "pdf",
            "enabled": True,
            "emailSubject": "Report Pagina del {{meta.scheduledAt}}",
            "emailBody": "<p>Test invio schedulazione automatica via API.</p>",
            "emailBodyFormat": "html"
        }
        response = api_context.post("/api/reports/schedules", data=payload)
        assert_status(response, 200)

    def test_schedules_endpoints_senza_auth_401(self, api_context_no_auth):
        assert_unauthorized(api_context_no_auth, "get", "/api/reports/schedules")
        assert_unauthorized(api_context_no_auth, "get", "/api/ftp/connections")


# per eseguire script: $env:API_DISCOVERY=1; pytest tests/7_report_e_analytics/test_schedulazioni.py --headed -s
# per eseguire test: pytest tests/api/7_report_e_analytics/test_schedulazioni_api.py -v