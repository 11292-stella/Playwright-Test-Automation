import pytest
from support.api_helpers import assert_status, assert_unauthorized


class TestReportAPI:
    """
    Test API per il modulo Report & Analytics (Template e Preview/Render)
    """

    def test_get_reports_datasets_status_200(self, api_context):
        response = api_context.get("/api/reports/datasets")
        assert_status(response, 200)

    def test_get_reports_templates_status_200(self, api_context):
        response = api_context.get("/api/reports/templates", params={"isGlobal": "false"})
        assert_status(response, 200)

    def test_get_reports_templates_global_status_200(self, api_context):
        response = api_context.get("/api/reports/templates", params={"isGlobal": "true"})
        assert_status(response, 200)

    def test_get_dataset_schema_and_fields_status_200(self, api_context):
        for dataset in ["SALES_MASTER", "STAFF_PERFORMANCE"]:
            res_schema = api_context.get(f"/api/reports/templates/datasets/{dataset}/schema")
            assert_status(res_schema, 200)

            res_sort = api_context.get(f"/api/reports/datasets/{dataset}/sortable-fields")
            assert_status(res_sort, 200)

            res_filter = api_context.get(f"/api/reports/datasets/{dataset}/filterable-fields")
            assert_status(res_filter, 200)

    def test_post_reports_preview_status_200(self, api_context):
        payload = {
            "templateId": "preview",
            "isGlobal": False,
            "html": "<h1>Test Report</h1><p>{{meta.tenantName}}</p>",
            "datasetType": "STAFF_PERFORMANCE",
            "masterTemplate": "default-master.html",
            "queryParams": {
                "dateFrom": "2026-06-19",
                "dateTo": "2026-08-16",
                "granularity": "week",
                "limit": 200
            }
        }
        response = api_context.post("/api/reports/preview", data=payload)
        assert_status(response, 200)

    def test_post_reports_template_creation_status_200(self, api_context):
        payload = {
            "name": "Report API Test Automatico",
            "description": "Template generato tramite test API.",
            "html": "<h1>Template API</h1>",
            "xlsxTemplate": "",
            "queryConfig": {
                "dateFrom": "2026-06-19",
                "dateTo": "2026-08-16",
                "granularity": "week",
                "limit": 200
            },
            "parameters": [
                {"key": "dateRange", "label": "Periodo", "type": "dateRange", "required": True}
            ],
            "customHeader": {"title": "Header Test", "subtitle": "Sottotitolo", "logoUrl": "", "align": "left"},
            "customFooter": {"text": "Footer Test", "showDate": True, "showPageNumber": True},
            "masterTemplate": "default-master.html",
            "datasetType": "STAFF_PERFORMANCE"
        }
        response = api_context.post("/api/reports/templates", data=payload)
        assert_status(response, 200)

    def test_reports_endpoints_senza_auth_401(self, api_context_no_auth):
        assert_unauthorized(api_context_no_auth, "get", "/api/reports/datasets")
        assert_unauthorized(api_context_no_auth, "get", "/api/reports/templates", params={"isGlobal": "false"})


    # per eseguire il test pytest tests/api/7_report_e_analytics/test_report_api.py -v
    # per eseguire lo script: $env:API_DISCOVERY=1; pytest tests/7_report_e_analytics/test_report.py --headed -s