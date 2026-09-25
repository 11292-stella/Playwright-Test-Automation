from playwright.sync_api import Page, expect
from pages.base_page import BasePage
import re


class SpeseOperative(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # --- NUOVA SPESA OPERATIVA ---
        self.btn_nuova_spesa_operativa = page.get_by_role("button", name="Nuova Spesa")
        self.combobox_categoria = page.get_by_role("combobox", name="Categoria *")
        self.input_descrizione = page.get_by_role("textbox", name="Descrizione *")
        self.input_imponibile = page.get_by_role("spinbutton", name="Imponibile *")
        self.dropdown_aliquota_iva = page.locator("div").filter(has_text=re.compile(r"^22%$")).first
        self.input_data = page.get_by_label("Data *", exact=True)
        self.input_data_scadenza = page.get_by_label("Data Scadenza", exact=True)
        self.input_fornitore = page.get_by_role("textbox", name="Fornitore")
        self.input_numero_fattura = page.get_by_role("textbox", name="Numero Fattura")
        self.textarea_note = page.get_by_role("textbox", name="Note")
        self.btn_annulla = page.get_by_role("button", name="Annulla", exact=True)
        self.btn_salva = page.get_by_role("button", name="Crea Spesa")

# ============================================================
# NAVIGAZIONE
# ============================================================

    def apri_spese_operative(self):
        self.apri_gruppo_menu("Controllo Gestione")
        self.naviga_a("/cost-control/operating-expenses")

# ============================================================
# NUOVA SPESA OPERATIVA
# ============================================================

    def compila_nuova_spesa(self, dati: dict):
        self.btn_nuova_spesa_operativa.click()

        self.seleziona_option_casuale_dropdown_icona_in_modale(self.combobox_categoria)

        self.input_descrizione.fill(dati["descrizione"])
        self.input_imponibile.fill(str(dati["imponibile"]))

        self.seleziona_option_casuale_dropdown_icona_in_modale(self.dropdown_aliquota_iva)

        self.compila_data(self.input_data, dati["data"])

        if dati.get("data_scadenza"):
            self.compila_data(self.input_data_scadenza, dati["data_scadenza"])

        if dati.get("fornitore"):
            self.input_fornitore.fill(dati["fornitore"])

        if dati.get("numero_fattura"):
            self.input_numero_fattura.fill(dati["numero_fattura"])

        if dati.get("note"):
            self.textarea_note.fill(dati["note"])

        self.btn_salva.click()