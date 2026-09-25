from playwright.async_api import Page
from pages.base_page import BasePage

class Fornitori(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # --- SWITCH ACQUISTABILI PER ATTIVARE TAB FORNITORI ---
        self.click_nuovo_prodotto = page.get_by_role("button", name="Nuovo Prodotto").first
        self.click_switch_acquistabili = page.get_by_role("checkbox", name="Acquistabile")

        # --- CERCA TAB FORNITORI ---
        self.cerca_tab_fornitori = page.locator(".v-slide-group__next > .mdi-chevron-right")
        self.click_tab_fornitori = page.get_by_role("tab", name="Fornitori")
        self.click_nuovo_fornitore = page.get_by_role("button", name="Aggiungi Fornitore")

        # --- AGGIUNGI FORNITORE CRASH ---
        self.seleziona_gruppo = page.locator(
            ".v-field.v-field--appended.v-field--center-affix.v-field--prepended.v-field--variant-filled"
        ).last.locator("input")

        # --- COMPILA MOD FORNITORE ---
        self.codice_articolo_fornitore = page.get_by_role("textbox", name="Cod. Articolo Fornitore")
        self.prezzo_unitario_fornitore = page.get_by_role("spinbutton", name="Prezzo Unitario")
        self.quantita_ordine_fornitore = page.get_by_role("spinbutton", name="Quantità Minima Ordine")
        self.lead_time = page.get_by_role("spinbutton", name="Lead Time (giorni)")
        self.click_aggiungi = page.get_by_role("button", name="Aggiungi", exact=True)

        # --- COMPILA_MODULO_SOTTOSTANTE ---
        self.conf_acquisto = page.get_by_role("textbox", name="Conf. Acquisto")
        self.fattore_conversione = page.get_by_role("spinbutton", name="Fattore Conversione")
        self.dropdown_unita_di_misura = page.get_by_label("UdM AcquistoUdM AcquistoUnità misura per ordini")
        self.click_creazione_finale_fornitori = page.get_by_role("button", name="Crea Prodotto")

    # --- NAVIGAZIONE ---
    def apri_catalogo(self):
            self.apri_gruppo_menu("Catalogo")
            self.naviga_a("/products")

    # --- SWITCH ACQUISTABILI PER ATTIVARE TAB FORNITORI ---

    def seleziona_acquistabili(self):
         self.click_nuovo_prodotto.click()
         self.click_switch_acquistabili.click()

    def cerca_e_seleziona_tab_fornitori(self):
         self.cerca_tab_fornitori.click()
         self.click_tab_fornitori.click()
         self.click_nuovo_fornitore.click()

    def cerca_e_seleziona_fornitore(self, nome_gruppo:str):
            self.seleziona_gruppo.click()
            self.seleziona_gruppo.fill(nome_gruppo)
    
            opzione = self.page.get_by_text(nome_gruppo)
            opzione.wait_for(state="visible")
            opzione.click()

    def compila_mod_fornitore(self,dati_fornitore:dict):
          self.codice_articolo_fornitore.fill(str(dati_fornitore["codice_articolo"]))
          self.prezzo_unitario_fornitore.fill(str(dati_fornitore["prezzo_unitario"]))
          self.quantita_ordine_fornitore.fill(str(dati_fornitore["quantita_minima"]))
          self.lead_time.fill(str(dati_fornitore["lead_time"]))
          self.click_aggiungi.click()


    def compila_mod_sotto(self,dati_fornitore:dict):
          self.conf_acquisto.fill(str(dati_fornitore["conf_acquisto"]))
          self.fattore_conversione.fill(str(dati_fornitore["fattore_conv"]))
          self.click_creazione_finale_fornitori.click()
          
            
