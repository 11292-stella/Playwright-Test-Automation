import pytest
from support.api_helpers import assert_status, assert_unauthorized, assert_field


@pytest.fixture
def categoria_di_test(api_context, faker):
    """
    Crea una categoria con nome univoco per il test corrente, così i
    test di lettura (fiscal-rules) hanno un dato proprio da usare
    invece di dipendere da categorie create a mano nel browser.
    """
    payload = {
        "name": faker.unique.word(),
        "parentId": None,
        "description": "categoria di test (creata da pytest)",
    }
    response = api_context.post("/v1/categories", data=payload)
    assert_status(response, 200)
    return response.json()


class TestGestioneCategorieAPI:
    """
    Test API per il modulo Gestione Categorie (mod_0_stabilita_moduli_cypress).
    Endpoint: /v1/categories
    Individuato con support/discover_endpoints.py.
    """

    def test_lista_categorie_status_200(self, api_context):
        response = api_context.get("/v1/categories")
        assert_status(response, 200)

    def test_crea_categoria_status_200(self, categoria_di_test):
        assert_field(categoria_di_test, "name")

    def test_recupera_fiscal_rules_categoria_status_200(self, api_context, categoria_di_test):
        
        nome = categoria_di_test["name"]
        response = api_context.get(f"/v1/categories/{nome}/fiscal-rules")
        assert_status(response, 200)

    def test_lista_categorie_senza_auth_401(self, api_context_no_auth):
        assert_unauthorized(api_context_no_auth, "get", "/v1/categories")

        # per eseguire: pytest tests/api/0_stabilita_moduli_cypress/test_gestione_categorie_api.py -v