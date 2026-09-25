from support.api_helpers import assert_status, assert_unauthorized


class TestWebAppAsportoBrandingAPI:
    """
    Test API per il modulo Webapp Asporto - Branding (mod_3_configurazione_ristorante_mod_webapp).
    Endpoint: GET /api/configurations/restaurant/webapp-asporto-branding,
    POST /api/configurations/restaurant/copy-branding,
    GET /api/numeratori.
    Individuati con support/discover_endpoints.py usando il bottone
    "Copia da App Asporto".
    """

    def test_webapp_asporto_branding_status_200(self, api_context):
        response = api_context.get("/api/configurations/restaurant/webapp-asporto-branding")
        assert_status(response, 200)

    def test_copia_branding_da_app_risponde_200_ma_non_applica_bug_noto(self, api_context):
        """
        BUG NOTO (già annotato in Web_App_Asporto_BrandingPage.py): il
        bottone "Copia da App Asporto" (POST copy-branding) risponde
        sempre 200 e non genera eccezioni, ma il dato copiato non viene
        realmente applicato — verificato anche manualmente con la
        console/Network aperta. Qui lo documentiamo lato API: la
        configurazione webapp-asporto-branding prima e dopo la copia
        risulta identica. Quando il bug verrà risolto questo assert
        fallirà in modo visibile: a quel punto va invertito, verificando
        che il campo copiato (es. tema) sia effettivamente cambiato.
        """
        prima = api_context.get("/api/configurations/restaurant/webapp-asporto-branding").json()

        payload = {
            "source": "app",
            "target": "webapp",
            "sections": ["theme", "texts", "images", "socialMedia"],
        }
        response = api_context.post("/api/configurations/restaurant/copy-branding", data=payload)
        assert_status(response, 200)

        dopo = api_context.get("/api/configurations/restaurant/webapp-asporto-branding").json()
        assert dopo == prima, (
            "La configurazione webapp-asporto-branding è cambiata dopo la copia: "
            "il bug 'copia che non applica' sembra risolto. Invertire questo "
            "assert e verificare invece che i campi copiati siano stati aggiornati."
        )

    def test_lista_numeratori_status_200(self, api_context):
        response = api_context.get("/api/numeratori")
        assert_status(response, 200)

    def test_webapp_asporto_branding_senza_auth_401(self, api_context_no_auth):
        assert_unauthorized(
            api_context_no_auth, "get", "/api/configurations/restaurant/webapp-asporto-branding"
        )

    def test_copia_branding_senza_auth_401(self, api_context_no_auth):
        payload = {
            "source": "app",
            "target": "webapp",
            "sections": ["theme", "texts", "images", "socialMedia"],
        }
        assert_unauthorized(
            api_context_no_auth, "post", "/api/configurations/restaurant/copy-branding", data=payload
        )

        # per eseguire: pytest tests/api/3_configurazione_ristorante_mod_webapp/test_web_app_asporto_branding_api.py -v
        # per eseguire script per endpoint: python -m support.discover_endpoints