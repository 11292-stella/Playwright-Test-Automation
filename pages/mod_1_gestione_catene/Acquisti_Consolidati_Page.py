from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class AcquistiPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # --- ELEMENTI ACQUISTI PAGE ---
        self.select_catena = page.get_by_label("Catena")
        self.btn_fabbisogno = page.get_by_role("button", name="Calcola fabbisogno")

    # --- NAVIGAZIONE ---

    def apri_acquisti(self):
        self.apri_gruppo_menu("Gestione catene")
        self.naviga_a("/chain-purchasing")

    # --- AZIONI ACQUISTI ---

    def filtra_per_catena(self, nome_catena: str):
        self.seleziona_option_per_testo_dropdown(self.select_catena, nome_catena)

    def click_fabbisogno(self):
        """Clicca il bottone 'Calcola fabbisogno' e attende il completamento del calcolo."""
        self.btn_fabbisogno.click()
        self.attendi_scomparsa_loader()
    