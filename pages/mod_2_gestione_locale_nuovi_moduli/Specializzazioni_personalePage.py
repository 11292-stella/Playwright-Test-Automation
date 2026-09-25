from playwright.sync_api import Page, expect
from pages.base_page import BasePage

class SpecializzazioniPersonalePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # --- ELEMENTI PAGINA ---
        self.btn_nuova_specializzazione = page.get_by_role("button", name="Nuova specializzazione")
        # --- ELEMENTI MODULO ---
        self.nome_specializzazione = page.get_by_role("textbox", name="Nome")
        self.descrizione_specializzazione = page.get_by_role("textbox", name="Descrizione")
        self.icona_specializzazione = page.get_by_role("textbox", name="Icona")
        self.ordine_specializzazione = page.get_by_role("spinbutton", name="Ordine")
        self.btn_crea_specializzazione = page.get_by_role("button", name="Crea")

        # --- VAI AL MODULO OPERATORI ---
        self.btn_modulo_operatori = page.get_by_role("link", name="Vai agli operatori")

        # --- CREA OPERATORE E ASSEGNA SPECIALIZZAZIONE ---
        self.btn_nuovo_operatore = page.get_by_role("button", name="Nuovo Operatore")
        self.input_nome = page.get_by_role("textbox", name="Nome*", exact=True)
        self.input_cognome = page.get_by_role("textbox", name="Cognome*")
        self.input_pin = page.get_by_role("textbox", name="PIN (4 cifre)*")
        self.input_costo = page.get_by_role("spinbutton", name="Costo Orario (€)")
        # --- PROFILO PER SERVIZI SU APPUNTAMENTO ---
        self.btn_profilo_servizi_appuntamento = page.get_by_role("button", name="Profilo per servizi su")
        self.combobox_specializzazioni = page.get_by_role("combobox", name="Specializzazioni")
        self.abilita_switch_prenotabile = page.get_by_role("checkbox", name="Prenotabile online dai clienti")
        self.descrizione_mod_prenotabile = page.get_by_role("textbox", name="Presentazione")
        self.btn_salvataggio_finale = page.get_by_role("button", name="Salva")

        # --- NAVIGAZIONE ---
    def apri_specializzazioni_personale(self):
        self.apri_gruppo_menu("Gestione Locale")
        self.naviga_a("/operators/specializations")

        # --- CREA NUOVA SPECIALIZZAZIONE ---
    def crea_nuova_specializzazione(self):
        self.btn_nuova_specializzazione.click()
        

        # --- COMPILAZIONE MODULO ---
    def compila_modulo_specializzazione(self, dati_specializzazione:dict):
        self.nome_specializzazione.fill(dati_specializzazione["nome_specializzazione"])
        self.descrizione_specializzazione.fill(dati_specializzazione["descrizione_specializzazione"])
        self.icona_specializzazione.fill(dati_specializzazione["icona_specializzazione"])
        self.ordine_specializzazione.fill(str(dati_specializzazione["ordine_specializzazione"]))
        self.btn_crea_specializzazione.click()

    def click_vai_a_operatori(self):
        self.btn_modulo_operatori.click()

        # --- CREA OPERATORE E ASSEGNA SPECIALIZZAZIONE ---

    def crea_e_compila_nuovo_operatore_con_specializzazione(self,dati_operatore:dict):
        self.btn_nuovo_operatore.click()
        self.input_nome.fill(dati_operatore["nome"])
        self.input_cognome.fill(dati_operatore["cognome"])
        self.input_pin.fill(dati_operatore["pin"])
        self.input_costo.fill(str(dati_operatore["costo"]))
      

        # --- ASSEGNAZIONE SPECIALIZZAZIONI ALL'OPERATORE ---

    def espandi_profilo_servizi_appuntamento(self):
        """Espande la sezione 'Profilo per servizi su appuntamento' nella scheda operatore,
        dove si trova il campo per assegnare le specializzazioni."""
        self.btn_profilo_servizi_appuntamento.click()

    def seleziona_specializzazioni(self, nomi_specializzazioni: list[str]):
        """Apre il combobox multi-select 'Specializzazioni' e seleziona più opzioni
        in sequenza. Il menu Vuetify resta aperto tra una selezione e l'altra
        (comportamento tipico dei combobox multi-select con chip), quindi non serve
        riaprirlo ad ogni click.

        :param nomi_specializzazioni: lista di nomi da selezionare, es.
                                    ["Cucina Vegana", "Sommelier", "Pasticcere"]
        """
        self.combobox_specializzazioni.click()
        for nome in nomi_specializzazioni:
            self.page.get_by_text(nome).click()
        self.page.keyboard.press("Escape")

    def click_e_completa_dopo_switch(self,dati_mod:dict):
        self.abilita_switch_prenotabile.click()
        self.descrizione_mod_prenotabile.fill(dati_mod["descrizione_mod"])
        self.btn_salvataggio_finale.click()