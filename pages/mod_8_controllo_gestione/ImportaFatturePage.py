from playwright.sync_api import Page, expect
from pages.base_page import BasePage
import re


class ImportFatture(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # --- CARICA FATTURA ELETTRONICA ---
        self.btn_carica_fattura = page.get_by_role("button", name="Carica Fattura")
        self.input_file = page.locator('input[type="file"]')
        self.btn_annulla = page.get_by_role("button", name="Annulla", exact=True)
        self.btn_carica = page.get_by_role("button", name="Carica", exact=True)

          # --- MAPPING ARTICOLI ---
        
        self.combobox_destinazione = page.get_by_role("combobox", name="Seleziona ingrediente o")
        self.checkbox_salva_mapping = page.get_by_role("checkbox", name="Salva mapping per acquisti")
        self.btn_conferma_aggiorna_costi = page.get_by_role("button", name="Conferma e Aggiorna Costi")
        self.input_elimina = page.locator(".v-btn.v-btn--icon.v-theme--posTheme.text-error")
        self.secondo_elimina = page.get_by_role("button", name="Elimina")
        

# ============================================================
# NAVIGAZIONE
# ============================================================

    def apri_import_fatture(self):
        self.apri_gruppo_menu("Controllo Gestione")
        self.naviga_a("/cost-control/invoices")

# ============================================================
# CARICA FATTURA ELETTRONICA
# ============================================================

    def carica_fattura(self, percorso_file: str):
        self.btn_carica_fattura.click()
        self.input_file.set_input_files(percorso_file)

        expect(self.btn_carica).to_be_enabled()
        self.btn_carica.click()

# ============================================================
# MAPPING ARTICOLI
# ============================================================

    def completa_mapping_articoli(self):

        self.checkbox_salva_mapping.click()

        self.seleziona_suggerimento_casuale_dropdown_in_modale(self.combobox_destinazione)

        
        self.btn_conferma_aggiorna_costi.click()
        self.input_elimina.click()
        self.secondo_elimina.click()