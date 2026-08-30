from pages.mod_3_configurazione_ristorante_mod_webapp.Web_App_Asporto_CatalogoPage import WebAppAsportoCatalogo

class TestWebAppAsportoCatalogo:
    def test_web_app_asporto_catalogo(self,authenticated_page):
        asporto = WebAppAsportoCatalogo(authenticated_page)
        asporto.apri_app_asporto_catalogo()

        asporto.copia_da_web_app_tavolo()

# per avviare tutti: pytest tests/3_configurazione_ristorante_mod_webapp/test_web_app_asporto_catalogo.py --headed