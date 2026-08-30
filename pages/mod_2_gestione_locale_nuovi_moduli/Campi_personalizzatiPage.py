from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class CampiPersonalizzati(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # --- NUOVO CAMPO ---
        self.btn_nuovo_campo = page.get_by_role("button", name="Nuovo campo")
        self.btn_salva_campo = page.get_by_role("button", name="Crea")

        # --- COMPILAZIONE CAMPO NUOVO ---
        self.input_etichetta = page.get_by_role("textbox", name="Etichetta")
        self.input_gruppo = page.get_by_role("textbox", name="Gruppo")
        self.input_descrizione = page.get_by_role("textbox", name="Descrizione")
        self.input_lunghezza = page.get_by_role("spinbutton", name="Lunghezza massima")
        self.input_formato_richiesto = page.get_by_role("textbox", name="Formato richiesto")
        self.select_tipo_dato = page.get_by_label("Tipo di dato")

        # --- CAMPI EXTRA: MIN/MAX NUMERICO ---
        self.input_valore_minimo = page.get_by_role("spinbutton", name="Valore minimo")
        self.input_valore_massimo = page.get_by_role("spinbutton", name="Valore massimo")

        # --- CAMPI EXTRA: OPZIONI ---
        self.btn_aggiungi_opzione = page.get_by_role("button", name="Aggiungi opzione")
        # niente locator fisso per "Etichetta opzione": sono N, li prendo dinamicamente

        # --- CAMPI EXTRA: SELEZIONE MULTIPLA ---
        self.input_selezioni_minime = page.get_by_role("spinbutton", name="Selezioni minime")
        self.input_selezioni_massime = page.get_by_role("spinbutton", name="Selezioni massime")

        # --- CAMPI EXTRA: DIARIO ---
        self.input_caratteri_per_voce = page.get_by_role("spinbutton", name="Caratteri per voce")
        self.input_voci_conservate = page.get_by_role("spinbutton", name="Voci conservate")

        # --- OPZIONI VISIBILITÀ / COMPORTAMENTO CAMPO ---
        self.chk_obbligatorio = page.get_by_role("checkbox", name="Obbligatorio")
        self.chk_ricercabile = page.get_by_role("checkbox", name="Ricercabile")
        self.chk_dato_personale = page.get_by_role("checkbox", name="Dato personale")
        self.chk_cassa = page.get_by_role("checkbox", name="Cassa")
        self.chk_registrazione_web = page.get_by_role("checkbox", name="Registrazione web")
        self.chk_portale_cliente = page.get_by_role("checkbox", name="Portale cliente")

        # --- MAPPATURA CHIAVE -> LABEL VISIBILE NELLA OPTION ---
        self.TIPO_DATO_LABELS = {
            "testo": "Testo",
            "testo_lungo": "Testo lungo",
            "numero_decimale": "Numero decimale",
            "numero_intero": "Numero intero",
            "importo": "Importo",
            "data": "Data",
            "data_ora": "Data e ora",
            "si_no": "Sì/No",
            "selezione_singola": "Selezione singola",
            "selezione_multipla": "Selezione multipla",
            "email": "Email",
            "telefono": "Telefono",
            "link": "Link",
            "diario": "Diario",
        }

        # --- DISPATCH: CHIAVE -> HANDLER ---
        self._dispatch_tipo_dato = {
            "numero_decimale": self.comp_per_numero_decimale,
            "numero_intero": self.comp_per_numero_decimale,   # stesso pattern
            "importo": self.comp_per_numero_decimale,          # stesso pattern
            "selezione_singola": self.comp_per_selezione_singola,
            "selezione_multipla": self.comp_per_selezione_multipla,
            "diario": self.comp_per_selezione_diario,
            # i tipi senza campi extra semplicemente non compaiono qui
        }

    # --- NAVIGAZIONE ---
    def apri_campi_personalizzati(self):
        self.apri_gruppo_menu("Gestione Locale")
        self.naviga_a("/settings/custom-fields")

    # --- CREA NUOVO CAMPO ---
    def crea_nuovo_campo(self):
        self.btn_nuovo_campo.click()

    # --- COMPILA CAMPO ---
    def compila_campo(self, dati_campo: dict):
        self.input_etichetta.fill(dati_campo["etichetta"])
        self.input_gruppo.fill(dati_campo["gruppo"])
        self.input_descrizione.fill(dati_campo["descrizione"])
        self.input_lunghezza.fill(str(dati_campo["lunghezza"]))
        self.input_formato_richiesto.fill(dati_campo["formato"])
        

    # --- SELEZIONE TIPO DI DATO + DISPATCH CAMPI EXTRA ---
    def seleziona_tipo_dato(self, tipo_dato: str, dati_stato: dict | None = None):
        label = self.TIPO_DATO_LABELS[tipo_dato]
        self.seleziona_option_per_testo_dropdown(self.select_tipo_dato, label)

        handler = self._dispatch_tipo_dato.get(tipo_dato)
        if handler:
            handler(dati_stato or {})

    # --- HELPER CONDIVISI (privati) ---
    def _compila_min_max(self, dati_stato: dict):
        self.input_valore_minimo.fill(str(dati_stato["valore_minimo"]))
        self.input_valore_massimo.fill(str(dati_stato["valore_massimo"]))

    def _aggiungi_opzioni(self, etichette: list[str]):
        for etichetta in etichette:
            self.btn_aggiungi_opzione.click()
            # prendo l'ultima textbox appena creata (quella vuota)
            self.page.get_by_role("textbox", name="Etichetta opzione").last.fill(etichetta)

    # --- HANDLER PER TIPO (chiamano gli helper) ---
    def comp_per_numero_decimale(self, dati_stato: dict):
        self._compila_min_max(dati_stato)

    def comp_per_selezione_singola(self, dati_stato: dict):
        self._aggiungi_opzioni(dati_stato["etichette_opzioni"])  # lista, anche di 1 elemento

    def comp_per_selezione_multipla(self, dati_stato: dict):
        self._aggiungi_opzioni(dati_stato["etichette_opzioni"])
        self.input_selezioni_minime.fill(str(dati_stato["selezioni_minime"]))
        self.input_selezioni_massime.fill(str(dati_stato["selezioni_massime"]))

    def comp_per_selezione_diario(self, dati_stato: dict):
        self._aggiungi_opzioni(dati_stato["etichette_opzioni"])
        self.input_caratteri_per_voce.fill(str(dati_stato["caratteri_per_voce"]))
        self.input_voci_conservate.fill(str(dati_stato["voci_conservate"]))

    def seleziona_opzioni_visibilita(self):
        self.chk_obbligatorio.check()
        self.chk_ricercabile.check()
        self.chk_dato_personale.check()
        self.chk_cassa.check()
        self.chk_registrazione_web.check()
        self.chk_portale_cliente.check()

    

    def salva_campo(self):
        response = self.clicca_e_attendi_risposta(
            self.btn_salva_campo,
            "**/custom-fields",  
        )
        assert response.status in (200, 201), f"Salvataggio fallito: status {response.status}"

    # --- NAVIGAZIONE TRA TAB ---

    def vai_a_tab(self, nome_tab: str):
        btn_freccia_destra = self.page.locator(".mdi-chevron-right").first
        tab = self.page.get_by_role("tab", name=nome_tab)

        # se la tab non è ancora visibile, scrolla la tab bar finché non compare
        for _ in range(5):  # limite di sicurezza per evitare loop infiniti
            if tab.is_visible():
                break
            btn_freccia_destra.click()
        
        tab.click()

    # --- SMOKE TEST: CREAZIONE MINIMA ---
    def crea_campo_minimo(self, etichetta: str, descrizione: str):
        self.crea_nuovo_campo()
        self.input_etichetta.fill(etichetta)
        self.input_descrizione.fill(descrizione)
        self.salva_campo()