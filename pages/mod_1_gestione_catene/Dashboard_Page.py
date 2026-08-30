from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class DashboardPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # --- ELEMENTI DASHBOARD ---
        self.select_catena = page.get_by_label("Catena")

    # --- NAVIGAZIONE ---

    def apri_dashboard(self):
        """Naviga fino alla Dashboard di catena (Gestione catene > Dashboard)."""
        self.apri_gruppo_menu("Gestione catene")
        self.naviga_a("/chain-dashboard")

    # --- AZIONI DASHBOARD ---

    def filtra_per_catena(self, nome_catena: str):
        """Seleziona una catena specifica dal filtro dashboard."""
        self.seleziona_option_per_testo_dropdown(self.select_catena, nome_catena)