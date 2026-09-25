from support.api_helpers import assert_status, assert_unauthorized, assert_field


class TestWebAppTavoloBrandingAPI:
    """
    Test API per il modulo Configurazione Ristorante > Web App Tavolo >
    Branding (mod_3_configurazione_ristorante_mod_webapp).
    Endpoint individuati con l'API discovery agganciata al test E2E
    esistente (tests/3_configurazione_ristorante_mod_webapp/test_web_app_tavolo_branding.py):
      - GET  /api/configurations/restaurant/info
      - GET  /api/configurations/restaurant/webapp-branding
      - POST /api/configurations/restaurant/copy-branding
    """

    def test_recupera_info_ristorante_status_200(self, api_context):
        response = api_context.get("/api/configurations/restaurant/info")
        assert_status(response, 200)

    def test_recupera_webapp_branding_status_200(self, api_context):
        response = api_context.get("/api/configurations/restaurant/webapp-branding")
        assert_status(response, 200)

    def test_copia_branding_da_app_a_webapp_status_200(self, api_context):
        """
        Equivalente API di tavolo.copia_da_asporto() nel test E2E:
        copia le sezioni di branding dall'app (source) alla webapp
        tavolo (target).
        """
        payload = {
            "source": "app",
            "target": "webapp",
            "sections": ["theme", "texts", "images", "socialMedia"],
        }
        response = api_context.post("/api/configurations/restaurant/copy-branding", data=payload)
        assert_status(response, 200)

        # NB: non conosciamo ancora la forma esatta del body di risposta
        # (nel log -s la riga <<< di questa POST non è comparsa prima del
        # PASSED). Se vuoi assertion più precise, rilancia con -s e aggiungi
        # qui un assert_field(response.json(), "...") sui campi che vedi.

    def test_copia_branding_senza_auth_401(self, api_context_no_auth):
        payload = {
            "source": "app",
            "target": "webapp",
            "sections": ["theme", "texts", "images", "socialMedia"],
        }
        assert_unauthorized(
            api_context_no_auth, "post", "/api/configurations/restaurant/copy-branding", data=payload
        )

        # per eseguire: pytest tests/api/3_configurazione_ristorante_mod_webapp/test_web_app_tavolo_branding_api.py -v
        # per avviare il test con script di endpoint: $env:API_DISCOVERY=1 pytest tests/3_configurazione_ristorante_mod_webapp/test_web_app_tavolo_branding.py --headed -s




