from pages.mod_3_configurazione_ristorante_mod_webapp.Web_App_Asporto_BrandingPage import WebAppAsportoBranding
from utils.test_data import ChainTestData

class TestWebAppAsportoBranding:
    def test_asporto_web_app(self,authenticated_page):
        asporto = WebAppAsportoBranding(authenticated_page)
        asporto.apri_app_asporto_branding()

        asporto.copia_da_asporto()


# per avviare tutti: pytest tests/3_configurazione_ristorante_mod_webapp/test_web_app_asporto_branding.py --headed