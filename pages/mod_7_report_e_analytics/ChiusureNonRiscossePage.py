from playwright.sync_api import Page, expect
from pages.base_page import BasePage

class Chiusure(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # --- TAB PASTI DIPENDENTI ---
        self.tab_pasti_dipendenti = page.get_by_role("tab", name="Pasti dipendenti")

        # --- TAB ADDESTRAMENTO ---
        self.tab_addestramento = page.get_by_role("tab", name="Addestramento")

        # --- TAB REPORT GENERATI ---
        self.tab_report = page.get_by_role("tab", name="Report generati")
        self.btn_aggiorna = page.get_by_role("button", name="Aggiorna")

    def _bottone_anteprima_attivo(self):
        return self.page.locator(".v-window-item--active").get_by_role(
            "button", name="Anteprima", exact=True
        )

# ============================================================
# NAVIGAZIONE
# ============================================================

    def apri_chiusure_non_riscosse(self):
        self.apri_gruppo_menu("Report & Analytics")
        self.naviga_a("/reports/non-paid")

# ============================================================
# TAB AUTOCONSUMO TITOLARE
# ============================================================

    def aggiorna_anteprima(self):
        self._bottone_anteprima_attivo().click()

# ============================================================
# TAB PASTI DIPENDENTI
# ============================================================

    def vai_a_tab_pasti_dipendenti(self):
        self.tab_pasti_dipendenti.click()
        self._bottone_anteprima_attivo().click()

# ============================================================
# TAB ADDESTRAMENTO
# ============================================================

    def vai_a_tab_addestramento(self):
        self.tab_addestramento.click()
        self._bottone_anteprima_attivo().click()

# ============================================================
# TAB REPORT GENERATI
# ============================================================

    def vai_a_tab_report(self):
        self.tab_report.click()
        self.btn_aggiorna.click()
        