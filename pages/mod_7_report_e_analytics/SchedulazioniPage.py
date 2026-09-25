from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class Schedulazioni(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # --- NUOVA SCHEDULAZIONE ---
        self.btn_nuova_scheda = page.get_by_role("button", name="Nuova Schedulazione")
        self.input_nome = page.get_by_role("textbox", name="Nome *")
        self.select_template = page.get_by_label("Template *", exact=True)
        self.select_canali_invio = page.get_by_label("Canali di Invio *", exact=True)
        self.input_destinatari_email = page.get_by_role("combobox", name="Destinatari Email *")
        self.select_frequenza = page.get_by_label("Frequenza", exact=True)
        self.input_espressione_cron = page.get_by_role("textbox", name="Espressione Cron *")
        self.select_formato_report = page.get_by_label("Formato Report", exact=True)
        self.switch_abilitato = page.get_by_label("Abilitato", exact=True)
        self.input_oggetto_email = page.get_by_role("textbox", name="Oggetto Email (opzionale)")
        self.corpo_email = page.get_by_role("textbox").nth(3)
        self.btn_annulla = page.get_by_role("button", name="Annulla", exact=True)
        self.btn_crea = page.get_by_role("button", name="Crea", exact=True)

# ============================================================
# NAVIGAZIONE
# ============================================================

    def apri_schedulazioni(self):
        self.apri_gruppo_menu("Report & Analytics")
        self.naviga_a("/reports/schedules")

# ============================================================
# NUOVA SCHEDULAZIONE
# ============================================================

    def apri_nuova_schedulazione(self):
        self.btn_nuova_scheda.click()

    def seleziona_template(self):
        self.seleziona_prima_opzione_dropdown_icona(self.select_template)

    def seleziona_template(self):
         self.seleziona_prima_opzione_dropdown_icona_in_modale(self.select_template)

    def aggiungi_destinatari_email(self, indirizzi: list[str]):
        for indirizzo in indirizzi:
            self.input_destinatari_email.fill(indirizzo)
            self.input_destinatari_email.press("Enter")

    def seleziona_frequenza(self, testo_opzione: str):
        self.seleziona_option_per_testo_dropdown_icona(self.select_frequenza, testo_opzione)

    def compila_espressione_cron(self, espressione: str):
        self.input_espressione_cron.fill(espressione)

    def seleziona_formato_report(self, testo_opzione: str):
        self.seleziona_option_per_testo_dropdown_icona(self.select_formato_report, testo_opzione)

    def imposta_abilitato(self, abilitato: bool):
        if self.switch_abilitato.is_checked() != abilitato:
            self.switch_abilitato.click()

    def compila_oggetto_email(self, oggetto: str):
        self.input_oggetto_email.fill(oggetto)

    def compila_corpo_email(self, testo: str):
        self.corpo_email.fill(testo)

    def compila_nuova_schedulazione(self, dati: dict):
        self.input_nome.fill(dati["nome"])

        if dati.get("seleziona_template"):
            self.seleziona_template()

        for canale in dati.get("canali_invio_extra", []):
            self.seleziona_canale_invio(canale)

        self.aggiungi_destinatari_email(dati["destinatari_email"])

        if dati.get("frequenza"):
            self.seleziona_frequenza(dati["frequenza"])

        if dati.get("espressione_cron"):
            self.compila_espressione_cron(dati["espressione_cron"])

        if dati.get("formato_report"):
            self.seleziona_formato_report(dati["formato_report"])

        if "abilitato" in dati:
            self.imposta_abilitato(dati["abilitato"])

        if dati.get("oggetto_email"):
            self.compila_oggetto_email(dati["oggetto_email"])

        if dati.get("corpo_email"):
            self.compila_corpo_email(dati["corpo_email"])

   