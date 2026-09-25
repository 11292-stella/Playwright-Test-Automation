from playwright.sync_api import Page, expect
from pages.base_page import BasePage
import re

class CategorieCosto(BasePage):
    def __init__(self, page:Page):
        super().__init__(page)

        # --- NUOVA CATEGORIA ---
        self.btn_nuova_categoria = page.get_by_role("button", name="Nuova Categoria")
        self.input_codice = page.get_by_role("textbox", name="Codice *")
        self.input_nome = page.get_by_role("textbox", name="Nome *")
        self.input_iva = page.get_by_role("spinbutton", name="IVA %")
        self.input_icona = page.get_by_role("textbox", name="Icona")
        self.input_colore = page.get_by_role("textbox", name="Colore")
        self.btn_salva = page.get_by_role("button", name="Salva", exact=True)
        self.input_sotto_categoria = page.locator("tr:nth-child(52) > .text-end > button").first
        

        # --- DROPDOWN ---
        self.dropdown_categoria_padre = page.get_by_text("Categoria PadreCategoria Padre")
        self.dropdown_natura = page.locator("div").filter(has_text=re.compile(r"^Variabile$")).first
        self.dropdown_frequenza = page.locator("div").filter(has_text=re.compile(r"^Mensile$")).first

          


# ============================================================
# NAVIGAZIONE
# ============================================================

    def apri_categorie_costo(self):
        self.apri_gruppo_menu("Controllo Gestione")
        self.naviga_a("/cost-control/cost-categories")

# ============================================================
# NUOVA CATEGORIA
# ============================================================
    
    def compila_mod(self, dati_categoria: dict):
        self.btn_nuova_categoria.click()

        self.input_codice.fill(dati_categoria["codice"])
        self.input_nome.fill(dati_categoria["nome"])

        if dati_categoria.get("seleziona_categoria_padre"):
            self.seleziona_option_casuale_dropdown_icona_in_modale(self.dropdown_categoria_padre)

        self.seleziona_option_casuale_dropdown_icona_in_modale(self.dropdown_natura)
        self.seleziona_option_casuale_dropdown_icona_in_modale(self.dropdown_frequenza)

        self.input_iva.fill(str(dati_categoria["iva"]))
        self.input_icona.fill(dati_categoria["icona"])
        self.input_colore.fill(dati_categoria["colore"])
        self.btn_salva.click()
        self.input_sotto_categoria.click()
        self.input_codice.fill(dati_categoria["codice_sotto_categoria"])
        self.input_nome.fill(dati_categoria["nome_sotto_categoria"])
        self.btn_salva.click()