from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class CostoRicette(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # --- FILTRI ---
        self.dropdown_costo = page.get_by_label("Base costo")
        self.btn_genera_dati = page.get_by_role("button", name="Genera Dati")
        self.btn_ricalcola = page.get_by_role("button", name="Ricalcola Tutti")
        self.btn_aggiorna = page.get_by_role("button", name="Aggiorna")

# ============================================================
# NAVIGAZIONE
# ============================================================
    def apri_costo_ricette(self):
        self.apri_gruppo_menu("Controllo Gestione")
        self.naviga_a("/cost-control/recipes")

# ============================================================
# FILTRI
# ============================================================

    def selezione_random_costo(self):
        self.seleziona_option_casuale_dropdown_icona(self.dropdown_costo)
        self.attendi_scomparsa_loader()

    def genera_dati_costo(self):
        self.btn_genera_dati.click()
        self.attendi_scomparsa_loader()

    def ricalcola_costo(self):
        self.btn_ricalcola.click()
        self.attendi_scomparsa_loader()
        self.btn_aggiorna.click()
        self.attendi_scomparsa_loader()
        
