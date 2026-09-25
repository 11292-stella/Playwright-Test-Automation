import pytest
from support.api_helpers import assert_status, assert_field, assert_unauthorized


class TestAppAsportoServiziAPI:
    """
    Test API per il modulo App Asporto - Servizi (mod_3_configurazione_ristorante_mod_webapp).
    Endpoint: GET /api/configurations/restaurant/info,
    GET/PUT /api/configurations/restaurant/app-branding,
    GET /api/numeratori.
    Individuati con support/discover_endpoints.py navigando le tab
    App Asporto / Testi / Loghi e Immagini e salvando.
    """

    def test_info_ristorante_status_200(self, api_context):
        response = api_context.get("/api/configurations/restaurant/info")
        assert_status(response, 200)

    def test_app_branding_status_200(self, api_context):
        response = api_context.get("/api/configurations/restaurant/app-branding")
        assert_status(response, 200)

    def test_aggiorna_tagline_app_branding_status_200(self, api_context, faker):
        """
        Legge la configurazione app-branding esistente e ne modifica solo
        la tagline (con un valore univoco via faker), poi la salva:
        così il test scrive un dato proprio senza sovrascrivere il resto
        della configurazione (loghi, tema, testi, servizi, ecc.) come
        farebbe rimandare indietro un payload statico copiato a mano.
        """
        config_attuale = api_context.get("/api/configurations/restaurant/app-branding").json()
        nuova_tagline = faker.unique.catch_phrase()
        config_attuale.setdefault("texts", {}).setdefault("it", {})["tagline"] = nuova_tagline

        response = api_context.put("/api/configurations/restaurant/app-branding", data=config_attuale)
        assert_status(response, 200)
        assert_field(response.json()["texts"]["it"], "tagline", nuova_tagline)

    def test_lista_numeratori_status_200(self, api_context):
        response = api_context.get("/api/numeratori")
        assert_status(response, 200)

    def test_info_ristorante_senza_auth_401(self, api_context_no_auth):
        assert_unauthorized(api_context_no_auth, "get", "/api/configurations/restaurant/info")

    def test_app_branding_senza_auth_401(self, api_context_no_auth):
        assert_unauthorized(api_context_no_auth, "get", "/api/configurations/restaurant/app-branding")

        # per eseguire: pytest tests/api/3_configurazione_ristorante_mod_webapp/test_app_asporto_servizi_api.py -v
        # per eseguire script per endpoint: python -m support.discover_endpoints