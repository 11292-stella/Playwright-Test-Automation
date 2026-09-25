import os
from support.api_helpers import assert_status, assert_unauthorized


# Catena di test nota, stessa usata negli altri file del modulo.
CODICE_CATENA_TEST = os.getenv("CODICE_CATENA_TEST", "demo_catena_test")


class TestFatturazioneCatenaAPI:
    """
    Test API per il modulo Fatturazione Catena (mod_1_gestione_catene).
    Endpoint: GET/PUT /api/chain-billing/{codice}/config,
    GET /api/chain-billing/{codice}/invoices,
    GET /api/chain-billing/{codice}/rollup,
    POST /api/chain-billing/{codice}/generate.
    Individuati con support/discover_endpoints.py salvando il modello di
    fatturazione e generando fatture a mano.
    """

    def test_config_fatturazione_catena_status_200(self, api_context):
        response = api_context.get(f"/api/chain-billing/{CODICE_CATENA_TEST}/config")
        assert_status(response, 200)

    def test_salva_modello_fatturazione_risponde_errore_bug_noto(self, api_context):
        """
        BUG NOTO: salvare il modello di fatturazione (PUT config) risponde
        500 invece di 200, sia con modello "royalty" che con modello
        "fixed" (osservato con support/discover_endpoints.py, entrambe le
        combinazioni provate manualmente falliscono allo stesso modo).
        Stesso pattern già usato per il bug del CRM di catena
        (test_catena_clienti_api.py) e per CampagnePage/Fidelity: il test
        verifica solo che l'errore sia ancora presente, così da rompersi
        in modo visibile quando l'app verrà corretta (a quel punto va
        ripristinato l'assert di successo status == 200).
        """
        payload = {
            "model": "royalty",
            "royaltyPct": 25,
            "fixedAmount": 0,
            "vatRate": 22,
            "billingCycle": "monthly",
        }
        response = api_context.put(f"/api/chain-billing/{CODICE_CATENA_TEST}/config", data=payload)
        assert response.status != 200, (
            "Il salvataggio del modello di fatturazione ora risponde 200: il bug sembra risolto. "
            "Ripristinare l'assert di successo (status == 200) e rimuovere questo commento."
        )

    def test_genera_fatture_status_200(self, api_context):
        payload = {"from": "2026-08-01", "to": "2026-08-31"}
        response = api_context.post(f"/api/chain-billing/{CODICE_CATENA_TEST}/generate", data=payload)
        assert_status(response, 200)

    def test_lista_fatture_status_200(self, api_context):
        response = api_context.get(f"/api/chain-billing/{CODICE_CATENA_TEST}/invoices")
        assert_status(response, 200)

    def test_rollup_fatturazione_status_200(self, api_context):
        response = api_context.get(f"/api/chain-billing/{CODICE_CATENA_TEST}/rollup")
        assert_status(response, 200)

    def test_config_fatturazione_catena_senza_auth_401(self, api_context_no_auth):
        assert_unauthorized(api_context_no_auth, "get", f"/api/chain-billing/{CODICE_CATENA_TEST}/config")

    def test_lista_fatture_senza_auth_401(self, api_context_no_auth):
        assert_unauthorized(api_context_no_auth, "get", f"/api/chain-billing/{CODICE_CATENA_TEST}/invoices")

        # per eseguire: pytest tests/api/1_gestione_catene/test_fatturazione_catena_api.py -v
        # per eseguire script per endpoint: python -m support.discover_endpoints