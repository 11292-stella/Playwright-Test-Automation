from support.api_helpers import assert_status, assert_unauthorized


class TestFornitoriAPI:
    """
    Test API per il modulo Fornitori (mod_0_stabilita_moduli_cypress).
    Endpoint: GET /v1/suppliers
    Individuato con support/discover_endpoints.py durante la ricerca
    fornitore nella tab "Fornitori" di un prodotto.
    """

    def test_lista_fornitori_status_200(self, api_context):
        response = api_context.get("/v1/suppliers", params={"pageSize": "100", "isActive": "true"})
        assert_status(response, 200)

    def test_ricerca_fornitore_per_nome_status_200(self, api_context):
        response = api_context.get(
            "/v1/suppliers",
            params={"query": "Abernathy - Swift", "pageSize": "20", "isActive": "true"},
        )
        assert_status(response, 200)

    def test_lista_fornitori_senza_auth_401(self, api_context_no_auth):
        assert_unauthorized(
            api_context_no_auth, "get", "/v1/suppliers", params={"pageSize": "100", "isActive": "true"}
        )

        # per eseguire: pytest tests/api/0_stabilita_moduli_cypress/test_fornitori_api.py -v
        # per eseguire script per endpoint: python -m support.discover_endpoints