import os
from support.api_helpers import assert_status, assert_unauthorized


# Catena di test nota, stessa usata negli altri file del modulo.
CODICE_CATENA_TEST = os.getenv("CODICE_CATENA_TEST", "demo_catena_test")


class TestCatenaClientiAPI:
    """
    Test API per il modulo Catena Clienti / CRM di catena
    (mod_1_gestione_catene).
    Endpoint: GET/PUT /api/chain-crm/{codice}/config,
    GET /api/chain-crm/{codice}/customers.
    """

    def test_config_crm_catena_status_200(self, api_context):
        response = api_context.get(f"/api/chain-crm/{CODICE_CATENA_TEST}/config")
        assert_status(response, 200)


    def test_ricerca_clienti_catena_status_200(self, api_context):
        response = api_context.get(
            f"/api/chain-crm/{CODICE_CATENA_TEST}/customers", params={"search": "000"}
        )
        assert_status(response, 200)

    def test_config_crm_catena_senza_auth_401(self, api_context_no_auth):
        assert_unauthorized(api_context_no_auth, "get", f"/api/chain-crm/{CODICE_CATENA_TEST}/config")

    def test_ricerca_clienti_catena_senza_auth_401(self, api_context_no_auth):
        assert_unauthorized(
            api_context_no_auth,
            "get",
            f"/api/chain-crm/{CODICE_CATENA_TEST}/customers",
            params={"search": "000"},
        )

        # per eseguire: pytest tests/api/1_gestione_catene/test_catena_clienti_api.py -v
        # per eseguire script per endpoint: python -m support.discover_endpoints