from playwright.sync_api import Page, expect
from pages.base_page import BasePage

class Dashboard(BasePage):
    def __init__(self, page:Page):
        super().__init__(page)

        # --- FILTRI ---
        self.btn_settimana = page.get_by_role("button", name="Settimana")
        self.btn_mese = page.get_by_role("button", name="Mese")
        self.btn_trimestre = page.get_by_role("button", name="Trimestre")
        self.btn_anno = page.get_by_role("button", name="Anno")

        # --- GENERA DATI E AGGIORNA
        self.btn_genera_dati = page.get_by_role("button", name="Genera Dati")
        self.btn_aggiorna = page.get_by_role("button", name="Aggiorna")

# ============================================================
# NAVIGAZIONE
# ============================================================

    def apri_controllo_gestione(self):
        self.apri_gruppo_menu("Controllo Gestione")
        self.naviga_a("/cost-control")

# ============================================================
# FILTRI
# ============================================================

    def scegli_filtro(self):
        self.seleziona_opzione_casuale_tra_testi(["Settimana", "Mese", "Trimestre", "Anno"])
        self.attendi_scomparsa_loader()

# ============================================================
# GENERA E AGGIORNA
# ============================================================

    def genera_e_aggiorna_dati(self):
        self.btn_genera_dati.click()
        self.attendi_scomparsa_loader()
        self.btn_aggiorna.click()
        self.attendi_scomparsa_loader()