from playwright.sync_api import Page
from pages.base_page import BasePage

class WebAppTavoloBranding(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # --- APRI TAB ---
        self.apri_tab_app_tavolo = page.get_by_role("tab", name="Webapp Tavolo - Branding")

        # --- COPIA DA ASPORTO ---
        self.btn_copia_asporto = page.get_by_role("button", name="Copia da App Asporto")
        self.checkbox_prodotti = page.get_by_role("checkbox", name="Catalogo prodotti (visibilita")
        self.checkbox_categorie = page.get_by_role("checkbox", name="Catalogo categorie (")
        self.btn_copia = page.get_by_role("button", name="Copia", exact=True)


         # --- NAVIGAZIONE ---
    def apri_app_tavolo(self):
        self.apri_gruppo_menu("Gestione Locale")
        self.naviga_a("/restaurant-config")
        self.apri_tab_app_tavolo.click()

    def copia_da_asporto(self):
        self.btn_copia_asporto.click()
        self.checkbox_prodotti.click()
        self.checkbox_categorie.click()
        self.btn_copia.click()