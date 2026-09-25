import os
import pytest
from support.api_helpers import assert_status, assert_unauthorized, assert_field


# Catena di test nota, stessa usata in Acquisti Consolidati: serve per
# entrare in modalità "modifica catalogo" di una catena esistente.
CODICE_CATENA_TEST = os.getenv("CODICE_CATENA_TEST", "demo_catena_test")


@pytest.fixture
def categoria_catena_di_test(api_context, faker):
    """
    Crea una categoria con nome univoco (contesto Catalogo Catena > tab
    Categorie), così i test di lettura (fiscal-rules) hanno un dato
    proprio invece di dipendere da categorie create a mano nel browser.
    Stesso endpoint /v1/categories usato in Gestione Categorie (mod_0):
    qui viene raggiunto passando prima da "Attiva modifica catalogo"
    sulla catena selezionata.
    """
    payload = {
        "name": faker.unique.word(),
        "parentId": None,
        "description": "categoria catena di test (creata da pytest)",
    }
    response = api_context.post("/v1/categories", data=payload)
    assert_status(response, 200)
    return response.json()


class TestCatalogoCatenaAPI:
    """
    Test API per il modulo Catalogo Catena (mod_1_gestione_catene),
    limitati alla parte Categorie (le altre tab del catalogo — Prodotti,
    Ingredienti, Varianti, Listini — sono già coperte da moduli/test
    dedicati, non ripetute qui).
    Endpoint: GET /api/chains, GET /api/chains/{codice}/members,
    GET /v1/categories, POST /v1/categories,
    GET /v1/categories/{nome}/fiscal-rules.
    """

    def test_lista_catene_status_200(self, api_context):
        response = api_context.get("/api/chains", params={"page": "1", "pageSize": "1000"})
        assert_status(response, 200)

    def test_membri_catena_status_200(self, api_context):
        response = api_context.get(f"/api/chains/{CODICE_CATENA_TEST}/members")
        assert_status(response, 200)

    def test_lista_categorie_status_200(self, api_context):
        response = api_context.get("/v1/categories")
        assert_status(response, 200)

    def test_crea_categoria_catena_status_200(self, categoria_catena_di_test):
        assert_field(categoria_catena_di_test, "name")

    def test_recupera_fiscal_rules_categoria_catena_status_200(self, api_context, categoria_catena_di_test):
        nome = categoria_catena_di_test["name"]
        response = api_context.get(f"/v1/categories/{nome}/fiscal-rules")
        assert_status(response, 200)

    def test_lista_catene_senza_auth_401(self, api_context_no_auth):
        assert_unauthorized(
            api_context_no_auth, "get", "/api/chains", params={"page": "1", "pageSize": "1000"}
        )

    def test_lista_categorie_senza_auth_401(self, api_context_no_auth):
        assert_unauthorized(api_context_no_auth, "get", "/v1/categories")

        # per eseguire: pytest tests/api/1_gestione_catene/test_catalogo_catena_api.py -v
        # per eseguire script per endpoint: python -m support.discover_endpoints