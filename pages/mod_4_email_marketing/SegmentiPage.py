from playwright.sync_api import Page, expect
from pages.base_page import BasePage
import random

class Segmenti(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # --- NUOVO SEGMENTO ---
        self.btn_nuovo_segmento = page.get_by_role("button", name="Nuovo segmento")

        # --- COMPILA MODULO ---
        self.input_nome = page.get_by_role("textbox", name="Nome")
        self.input_descrizione = page.get_by_role("textbox", name="Descrizione")
        
        self.input_tag = page.get_by_role("combobox", name="Tag")
        self.input_gruppo_cliente = page.get_by_role("textbox", name="Gruppo cliente")
        self.input_citta = page.get_by_role("textbox", name="Città")
        self.input_da = page.get_by_role("spinbutton", name="Punti da")
        self.input_a = page.get_by_role("spinbutton", name="Punti a")

        # --- DROPDOWN TIPO ---
        self.testi_opzioni_tipo = [
             "Dinamico",
             "Statico"
        ]

        self.dropdown_tipo = self.dropdown_per_testo("Tipo")


        # --- DROPDOWN COMPLEANNO NEL MESE ---
        self.mesi_disponibili = [
            "Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno",
            "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre",
        ]

        self.dropdown_compleanno_mese = self.dropdown_per_testo("Compleanno nel mese")

        # --- DATE ISCRIZIONE ---
        self.input_iscritti_dal = page.get_by_role("textbox", name="Iscritti dal")
        self.input_iscritti_fino_al = page.get_by_role("textbox", name="Iscritti fino al")

        # --- DROPDOWN Lingua ---
        self.testi_opzioni_Lingua = [
                     "Italiano",
                     "English"
                ]
        
        self.dropdown_Lingua = self.dropdown_per_testo("Lingua")

        # --- CREAZIONE FINALE ---
        self.btn_crea_finale = page.get_by_role("button", name="Crea")




        # --- NAVIGAZIONE ---
    def apri_segmenti(self):
            self.apri_gruppo_menu("Email Marketing")
            self.naviga_a("/marketing/audiences")

        # --- NUOVO SEGMENTO ---
    def crea_nuovo_segmento(self):
         self.btn_nuovo_segmento.click()

         # --- COMPILA MODULO ---
    def compila_mod_nuovo_segmento(self, dati_segmento: dict):
        
        self.input_nome.fill(dati_segmento["nome"])
        self.input_descrizione.fill(dati_segmento["descrizione"])
        self.input_tag.fill(dati_segmento["tag"])
        self.input_gruppo_cliente.fill(dati_segmento["gruppo_cliente"])
        self.input_citta.fill(dati_segmento["citta"])
        self.input_da.fill(str(dati_segmento["punti_da"]))
        self.input_a.fill(str(dati_segmento["punti_a"]))
        self.compila_data(self.input_iscritti_dal, dati_segmento["iscritti_dal"])
        self.compila_data(self.input_iscritti_fino_al, dati_segmento["iscritti_fino_al"])
        self.btn_crea_finale.click()

    def seleziona_tipo_random(self):
         self.seleziona_option_per_testo_dropdown(self.dropdown_tipo, "Dinamico")

    def seleziona_mese_compleanno_random(self):
        """Seleziona un mese casuale dal multi-select 'Compleanno nel mese'.
        Chiude esplicitamente l'overlay dopo la selezione (Escape) invece di
        lasciarlo aperto, per lo stesso motivo già documentato sui v-select
        multiple: overlay aperto durante la crescita del campo chip può
        causare crash del renderer in CI headless."""
        mese_scelto = random.choice(self.mesi_disponibili)

        self.dropdown_compleanno_mese.click(force=True)
        self.page.get_by_role("option", name=mese_scelto, exact=True).click()
        self.page.keyboard.press("Escape")

    def selezione_lingua_random(self):
         self.seleziona_option_per_testo_dropdown(self.dropdown_Lingua,"Italiano")

    
    