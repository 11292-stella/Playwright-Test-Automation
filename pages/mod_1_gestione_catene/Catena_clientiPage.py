from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class ClientiPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # --- ELEMENTI CLIENTI PAGE ---
        self.clienti_catena = page.get_by_label("Catena")

        # --- TOGGLE / CONFIGURAZIONE ---
        self.toggle_catena = page.get_by_role("checkbox", name="CRM di catena attivo")
        self.btn_salva = page.get_by_role("button", name="Salva")
        self.banner_non_abilitato = page.get_by_text("CRM di catena non abilitato per questa catena")

    # --- NAVIGAZIONE ---

    def apri_clienti(self):
        """Naviga fino a Clienti Catena (Gestione catene > Clienti Catena)."""
        self.apri_gruppo_menu("Gestione catene")
        self.naviga_a("/chain-customers")

    # --- AZIONI CLIENTI CATENA ---

    def filtra_per_catena(self, nome_catena: str):
        """Seleziona una catena specifica dal filtro."""
        self.seleziona_option_per_testo_dropdown(self.clienti_catena, nome_catena)
        self.attendi_scomparsa_loader()

    def switch_toggle(self):
        self.toggle_catena.click()

    def attiva_e_salva_crm_catena(self):
        """Attiva (se non già attivo) il toggle 'CRM di catena attivo' e salva."""
        if not self.toggle_catena.is_checked():
            self.toggle_catena.click()
        self.btn_salva.click()
        self.attendi_scomparsa_loader()

    