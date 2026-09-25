import os
from support.api_helpers import assert_status, assert_unauthorized


# Catena di test nota, usata come nel test Fornitori (ricerca/filtro su un
# dato esistente invece di crearne uno: le catene non si creano in questa
# suite, sono un dato di setup dell'ambiente di test).
CODICE_CATENA_TEST = os.getenv("CODICE_CATENA_TEST", "demo_catena_test")
DATA_DA = "2026-08-17"
DATA_A = "2026-08-31"


class TestAcquistiConsolidatiAPI:
    """
    Test API per il modulo Acquisti Consolidati (mod_1_gestione_catene).
    Endpoint: GET /api/chains, GET /api/chain-purchasing/{codiceCatena}/demand.
    Individuati con support/discover_endpoints.py mentre si filtrava per
    catena e si calcolava il fabbisogno (bottone "Calcola fabbisogno").
    """

    def test_lista_catene_status_200(self, api_context):
        response = api_context.get("/api/chains", params={"page": "1", "pageSize": "1000"})
        assert_status(response, 200)

    def test_calcolo_fabbisogno_status_200(self, api_context):
        response = api_context.get(
            f"/api/chain-purchasing/{CODICE_CATENA_TEST}/demand",
            params={"from": DATA_DA, "to": DATA_A},
        )
        assert_status(response, 200)

    def test_lista_catene_senza_auth_401(self, api_context_no_auth):
        assert_unauthorized(
            api_context_no_auth, "get", "/api/chains", params={"page": "1", "pageSize": "1000"}
        )

    def test_calcolo_fabbisogno_senza_auth_401(self, api_context_no_auth):
        assert_unauthorized(
            api_context_no_auth,
            "get",
            f"/api/chain-purchasing/{CODICE_CATENA_TEST}/demand",
            params={"from": DATA_DA, "to": DATA_A},
        )

        # per eseguire: pytest tests/api/1_gestione_catene/test_acquisti_consolidati_api.py -v
        # per eseguire script per endpoint: python -m support.discover_endpoints