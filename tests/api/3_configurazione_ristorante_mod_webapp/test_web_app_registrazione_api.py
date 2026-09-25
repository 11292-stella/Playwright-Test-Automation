from support.api_helpers import assert_status, assert_unauthorized


class TestWebAppRegistrazioneAPI:
    """
    Test API per il modulo Webapp Registrazione Clienti (mod_3_configurazione_ristorante_mod_webapp).
    Endpoint: GET /api/configurations/restaurant/registration-webapp,
    GET /api/custom-fields/entity/customer/descriptors.
    Individuati con support/discover_endpoints.py aprendo la tab Webapp
    Registrazione Clienti.
    
    """

    def test_registration_webapp_status_200(self, api_context):
        response = api_context.get("/api/configurations/restaurant/registration-webapp")
        assert_status(response, 200)

    def test_descrittori_campi_registrazione_status_200(self, api_context):
        response = api_context.get(
            "/api/custom-fields/entity/customer/descriptors",
            params={"locale": "it", "scope": "registration"},
        )
        assert_status(response, 200)

    def test_registration_webapp_senza_auth_401(self, api_context_no_auth):
        assert_unauthorized(api_context_no_auth, "get", "/api/configurations/restaurant/registration-webapp")

    def test_descrittori_campi_registrazione_senza_auth_401(self, api_context_no_auth):
        assert_unauthorized(
            api_context_no_auth,
            "get",
            "/api/custom-fields/entity/customer/descriptors",
            params={"locale": "it", "scope": "registration"},
        )

        # per eseguire: pytest tests/api/3_configurazione_ristorante_mod_webapp/test_web_app_registrazione_api.py -v
        # per eseguire script per endpoint: python -m support.discover_endpoints