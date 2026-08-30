from playwright.sync_api import Page
from pages.base_page import BasePage

class WebAppAsportoCatalogo(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # --- APRI TAB ---
        self.apri_tab_app_asporto_catalogo = page.get_by_role("tab", name="Webapp Asporto - Catalogo")

        # --- COPIA DA ASPORTO ---
        self.btn_copia_da_tavolo = page.get_by_role("button", name="Copia da Webapp Tavolo")
        self.btn_copia = page.get_by_role("button", name="Copia", exact=True)
        self.btn_chiudi = page.get_by_role("button", name="Chiudi")

        # --- NAVIGAZIONE ---
    def apri_app_asporto_catalogo(self):
        self.apri_gruppo_menu("Gestione Locale")
        self.naviga_a("/restaurant-config")
        self.apri_tab_app_asporto_catalogo.click()

        # --- COPIA DA WEBAPP TAVOLO ---
    def copia_da_web_app_tavolo(self):
        self.btn_copia_da_tavolo.click()
        self.btn_copia.click()
        self.btn_chiudi.click()