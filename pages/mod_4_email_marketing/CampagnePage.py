from playwright.sync_api import Page, expect
from pages.base_page import BasePage
import re

class CampagneMarketing(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # --- BTN NUOVA CREAZIONE ---
        self.btn_nuova_campagna = page.get_by_role("button", name="Nuova campagna")

        # --- COMPILA PRIMO MODALE ---
        
        self.input_campo_vuoto = page.get_by_text("VuotoParti da un foglio bianco")
        self.btn_crea = page.get_by_role("button", name="Crea")

        # --- COMPILA SECONDO MODALE ---
        self.input_nome_campagna = page.get_by_role("textbox", name="Nome", exact=True)
        self.input_oggetto = page.get_by_role("textbox", name="Oggetto")
        self.input_nome_utente = page.get_by_role("textbox", name="Nome mittente")
        self.input_rispondi_a = page.get_by_role("textbox", name="Rispondi a")
        self.input_riga_anteprima = page.get_by_role("textbox", name="Anteprima nella casella di")
        self.box_tex = page.get_by_role("textbox").nth(5)
        self.input_orario_invio = page.get_by_role("textbox", name="Ora di invio")
        self.attiva_da = page.get_by_role("textbox", name="Attiva dal")
        self.fino_al = page.get_by_role("textbox", name="Fino al")  

        # --- SEGMENTO DESTINATARI ---
        self.dropdown_segmento_destinatari = page.get_by_role("combobox", name="Segmento destinatari")  

        # --- TAB ANTEPRIMA ---
        self.tab_anteprima = page.get_by_role("tab", name="Anteprima")
        # --- ANTEPRIMA ---
        self.btn_aggiorna_anteprima = page.get_by_role("button", name="Aggiorna anteprima")
        self.btn_anteprima_icona = page.get_by_role("button").filter(has_text=re.compile(r"^$")).nth(5)
        self.btn_anteprima_html = page.get_by_role("button", name="HTML")
        self.btn_anteprima_solo_testo = page.get_by_role("button", name="Solo testo")

        # --- PROVA INVIO ---
        self.btn_prova_invio = page.get_by_role("button", name="Prova")
        self.input_indirizzo_destinatario = page.get_by_role("textbox", name="Indirizzo di destinazione")
        self.btn_invia = page.get_by_role("button", name="Invia", exact=True)

        # --- PROVA PROGRAMMA ---
        self.btn_programma = page.get_by_role("button", name="Programma")
        self.input_data_e_ora = page.get_by_role("textbox", name="Data e ora")
        self.btn_crea_programma = page.get_by_role("dialog").get_by_role("button", name="Programma")

    # --- NAVIGAZIONE ---
    def apri_campagne_marketing(self):
       self.apri_gruppo_menu("Email Marketing")
       self.naviga_a("/marketing/campaigns")

    # --- NUOVA CAMPAGNA ---
    def crea_nuova_campagna(self):
        self.btn_nuova_campagna.click()

    # --- COMPILA MODULO ---
    def compila_mod_campagana(self,dati_modulo:dict):
        self.input_nome_campagna.fill(dati_modulo["nome_campagna"])
        self.input_campo_vuoto.click()
        self.btn_crea.click()

    def compila_secondo_modale(self, dati_campagna: dict):
        self.input_nome_campagna.fill(dati_campagna["nome_campagna"])
        self.input_oggetto.fill(dati_campagna["oggetto"])
        self.input_nome_utente.fill(dati_campagna["nome_mittente"])
        self.input_rispondi_a.fill(dati_campagna["rispondi_a"])
        self.input_riga_anteprima.fill(dati_campagna["riga_anteprima"])
        self.box_tex.fill(dati_campagna["messaggio"])
        self.input_orario_invio.fill(dati_campagna["orario_invio"])
        self.compila_data(self.attiva_da, dati_campagna["attiva_dal"])
        self.compila_data(self.fino_al, dati_campagna["fino_al"])

    def seleziona_primo_segmento_destinatari(self):
        self.seleziona_prima_opzione_dropdown_icona(self.dropdown_segmento_destinatari)

    # --- ANTEPRIMA TAB ---

    def vai_a_anteprima(self):
     self.tab_anteprima.click()

    def visualizza_tutte_anteprime(self):
        """Naviga il tab 'Anteprima' e clicca in sequenza tutte le modalità
        di visualizzazione disponibili (icona, HTML, Solo testo), dopo aver
        aggiornato l'anteprima."""
        self.btn_aggiorna_anteprima.click()
        self.btn_anteprima_icona.click()
        self.btn_anteprima_html.click()
        self.btn_anteprima_solo_testo.click()

    # --- PROVA INVIO ---
    def click_invio_prova(self):
        self.btn_prova_invio.click()
        self.input_indirizzo_destinatario.fill("demo.recipient@example.com")
        self.btn_invia.click()

    # --- PROGRAMMA ---
    def click_programma(self,dati_programma:dict):
        self.btn_programma.click()
        self.compila_data(self.input_data_e_ora, dati_programma["data_e_ora"])
        self.btn_crea_programma.click()
        