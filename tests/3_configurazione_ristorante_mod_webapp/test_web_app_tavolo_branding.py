from pages.mod_3_configurazione_ristorante_mod_webapp.Web_App_Tavolo_BrandingPage import WebAppTavoloBranding
from utils.test_data import ChainTestData

class TestWebAppTavolo:
    def test_app_tavolo(self,authenticated_page):
        tavolo = WebAppTavoloBranding(authenticated_page)
        tavolo.apri_app_tavolo()

        tavolo.copia_da_asporto()


# per avviare tutti: pytest tests/3_configurazione_ristorante_mod_webapp/test_web_app_tavolo_branding.py --headed