import os
import pytest
from support.api_helpers import assert_status, assert_unauthorized


# Catena di test nota, stessa usata negli altri file del modulo.
CODICE_CATENA_TEST = os.getenv("CODICE_CATENA_TEST", "demo_catena_test")
# Negozio sorgente noto, usato come nel test Fornitori/Ricetta per un
# dato esistente non creabile via API in questa suite.
TENANT_SORGENTE_TEST = os.getenv("TENANT_SORGENTE_TEST", "demo_tenant_test")


def _payload_import(dry_run: bool) -> dict:
    return {
        "sourceTenantId": TENANT_SORGENTE_TEST,
        "collections": ["variants"],
        "onlyLocalItems": True,
        "dryRun": dry_run,
    }


class TestImportaDaNegozioAPI:
    """
    Test API per il modulo Importa da Negozio (mod_1_gestione_catene).
    Endpoint: GET /api/chains, GET /api/tenants,
    POST /api/chain-catalog/{codice}/import-from-tenant.
    Individuati con support/discover_endpoints.py facendo prima
    un'anteprima (dryRun) e poi l'import vero e proprio a mano.
    """

    def test_lista_catene_status_200(self, api_context):
        response = api_context.get("/api/chains", params={"page": "1", "pageSize": "1000"})
        assert_status(response, 200)

    def test_lista_negozi_sorgente_status_200(self, api_context):
        response = api_context.get("/api/tenants", params={"pageSize": "500"})
        assert_status(response, 200)

    def test_anteprima_import_da_negozio_status_200(self, api_context):
        """
        Anteprima (dryRun=true): non modifica dati, ripetibile in
        automazione. Usata come test principale per l'import, mentre
        l'import reale (dryRun=false) non viene lanciato in automazione
        (vedi test successivo) per non alterare ripetutamente il
        catalogo condiviso della catena di test.
        """
        response = api_context.post(
            f"/api/chain-catalog/{CODICE_CATENA_TEST}/import-from-tenant",
            data=_payload_import(dry_run=True),
        )
        assert_status(response, 200)

    @pytest.mark.skip(
        reason=(
            "Import reale (dryRun=false): scrive dati nel catalogo della catena di "
            "test condivisa e non è idempotente/ripetibile come le altre azioni "
            "della suite (a differenza del DDT tabacchi, qui non risulta un "
            "comportamento di 'reused'). Da eseguire manualmente se serve "
            "verificarlo end-to-end."
        )
    )
    def test_import_reale_da_negozio_status_200(self, api_context):
        response = api_context.post(
            f"/api/chain-catalog/{CODICE_CATENA_TEST}/import-from-tenant",
            data=_payload_import(dry_run=False),
        )
        assert_status(response, 200)

    def test_lista_catene_senza_auth_401(self, api_context_no_auth):
        assert_unauthorized(
            api_context_no_auth, "get", "/api/chains", params={"page": "1", "pageSize": "1000"}
        )

    def test_anteprima_import_da_negozio_senza_auth_401(self, api_context_no_auth):
        assert_unauthorized(
            api_context_no_auth,
            "post",
            f"/api/chain-catalog/{CODICE_CATENA_TEST}/import-from-tenant",
            data=_payload_import(dry_run=True),
        )

        # per eseguire: pytest tests/api/1_gestione_catene/test_importa_da_negozio_api.py -v
        # per eseguire script per endpoint: python -m support.discover_endpoints