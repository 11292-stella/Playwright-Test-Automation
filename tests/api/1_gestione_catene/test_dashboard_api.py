import os
from support.api_helpers import assert_status, assert_unauthorized


# Catena di test nota, stessa usata negli altri file del modulo.
CODICE_CATENA_TEST = os.getenv("CODICE_CATENA_TEST", "demo_catena_test")
DATA_DA = "2026-08-01"
DATA_A = "2026-08-31"


class TestDashboardAPI:
    """
    Test API per il modulo Dashboard di catena (mod_1_gestione_catene).
    Endpoint: GET /api/chain-analytics/{codice}/overview,
    GET /api/chain-analytics/{codice}/timeseries,
    GET /api/chain-analytics/{codice}/food-cost,
    GET /api/chain-rollup/{codice}/today.
    Individuati con support/discover_endpoints.py filtrando la dashboard
    per catena.
    """

    def test_overview_dashboard_catena_status_200(self, api_context):
        response = api_context.get(
            f"/api/chain-analytics/{CODICE_CATENA_TEST}/overview",
            params={"from": DATA_DA, "to": DATA_A},
        )
        assert_status(response, 200)

    def test_timeseries_dashboard_catena_status_200(self, api_context):
        response = api_context.get(
            f"/api/chain-analytics/{CODICE_CATENA_TEST}/timeseries",
            params={"from": DATA_DA, "to": DATA_A},
        )
        assert_status(response, 200)

    def test_food_cost_dashboard_catena_status_200(self, api_context):
        response = api_context.get(
            f"/api/chain-analytics/{CODICE_CATENA_TEST}/food-cost",
            params={"periodType": "month"},
        )
        assert_status(response, 200)

    def test_rollup_oggi_catena_status_200(self, api_context):
        response = api_context.get(f"/api/chain-rollup/{CODICE_CATENA_TEST}/today")
        assert_status(response, 200)

    def test_overview_dashboard_catena_senza_auth_401(self, api_context_no_auth):
        assert_unauthorized(
            api_context_no_auth,
            "get",
            f"/api/chain-analytics/{CODICE_CATENA_TEST}/overview",
            params={"from": DATA_DA, "to": DATA_A},
        )

    def test_rollup_oggi_catena_senza_auth_401(self, api_context_no_auth):
        assert_unauthorized(api_context_no_auth, "get", f"/api/chain-rollup/{CODICE_CATENA_TEST}/today")

        # per eseguire: pytest tests/api/1_gestione_catene/test_dashboard_api.py -v
        # per eseguire script per endpoint: python -m support.discover_endpoints