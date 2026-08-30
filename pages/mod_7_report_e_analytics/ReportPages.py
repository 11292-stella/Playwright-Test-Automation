from playwright.sync_api import Page, expect
from pages.base_page import BasePage
import re

class Report(BasePage):

    # Mapping tra il valore tecnico del dataset (option value nel <select>)
    # e l'etichetta italiana mostrata realmente nei menu (scoperta via
    # debug_opzioni_tipo_dataset). Riusato sia nel filtro lista template
    # sia nel campo 'Tipo Dataset *' dell'editor: stessa lista di opzioni.
    ETICHETTE_TIPO_DATASET = {
        "SALES_MASTER": "Vendite Master",
        "SALES_TRENDS": "Trend Vendite",
        "PRODUCT_MIX": "Mix Prodotti",
        "INVENTORY_LOG": "Movimenti Magazzino",
        "STAFF_PERFORMANCE": "Performance Staff",
        "FIDELITY_INSIGHTS": "Programma Fidelity",
        "CUSTOMER_SEGMENT": "Segmentazione Clienti",
        "AUDIT_LOG": "Audit Log",
        "HOURLY_PERFORMANCE": "Performance Oraria",
        "BOOKINGS": "Prenotazioni",
        "CASH_X_REPORT": "Report X Cassa",
        "CASH_Z_REPORT": "Chiusura Z",
        "CASH_DAILY_SUMMARY": "Riepilogo Giornaliero Cassa",
        "CASH_VARIANCE": "Varianze Cassa",
        "CASH_OPERATOR_PERF": "Performance Operatori Cassa",
        "CASH_FLOW": "Flusso di Cassa",
        "PL_REPORT": "Conto Economico (P&L)",
        "FOOD_COST_ANALYSIS": "Analisi Food Cost",
        "DELIVERY_PERFORMANCE": "Performance Consegne",
        "OPERATING_EXPENSES_REPORT": "Costi Operativi",
        "TABLE_UTILIZATION": "Utilizzo Tavoli",
        "PAYMENT_TERMINAL_ANALYTICS": "Analisi Pagamenti",
        "SALES_BY_FISCAL_DEPARTMENT": "SALES BY FISCAL DEPARTMENT",
        "CASH_MOVEMENTS_HISTORICAL": "CASH MOVEMENTS HISTORICAL",
        "CASH_MOVEMENTS": "CASH MOVEMENTS",
        "BUDGET_VARIANCE_REPORT": "Scostamento Budget",
        "MENU_ENGINEERING_MATRIX": "MENU ENGINEERING MATRIX",
        "MARKET_BASKET": "MARKET BASKET",
        "CUSTOMER_COHORT": "CUSTOMER COHORT",
        "CUSTOMER_CLV": "CUSTOMER CLV",
        "ANOMALY_DETECTION": "ANOMALY DETECTION",
        "GYM_MEMBERSHIPS": "GYM MEMBERSHIPS",
        "GYM_ATTENDANCE": "GYM ATTENDANCE",
        "GYM_CLASS_SATURATION": "GYM CLASS SATURATION",
        "GYM_TRAINER_PRODUCTIVITY": "GYM TRAINER PRODUCTIVITY",
        "GYM_LEAD_FUNNEL": "GYM LEAD FUNNEL",
        "GYM_RETENTION": "GYM RETENTION",
    }

    # Etichette italiane delle opzioni del dropdown 'Granularità' (Test Parametri).
    ETICHETTE_GRANULARITA = {
        "day": "Giornaliero",
        "week": "Settimanale",
        "month": "Mensile",
    }

    # Etichette italiane delle opzioni del dropdown 'Allineamento Header'.
    ETICHETTE_ALLINEAMENTO_HEADER = {
        "left": "Sinistra",
        "center": "Centro",
        "right": "Destra",
    }

    def __init__(self, page: Page):
        super().__init__(page)

        # --- NUOVO REPORT CREAZIONE DA ZERO ---
        self.bottone_crea_template = page.get_by_role("button", name="Crea Template")

        # --- EDITOR: IMPOSTAZIONI TEMPLATE ---
        self.campo_nome_template = page.get_by_role("textbox", name="Nome Template *")
        self.select_tipo_dataset_editor = page.get_by_label("Tipo Dataset *", exact=True)
        self.select_master_template = page.get_by_label("Master Template", exact=True)
        self.campo_descrizione_template = page.get_by_role("textbox", name="Descrizione", exact=True)

                # --- EDITOR: TEST PARAMETRI ---
        self.campo_data_da = page.get_by_label("Data Da", exact=True)
        self.campo_data_a = page.get_by_label("Data A", exact=True)
        self.select_granularita = page.get_by_label("Granularità", exact=True)
        self.campo_limite_righe = page.get_by_role("spinbutton", name="Limite Righe")
        self.btn_aggiungi_criterio_ordinamento = page.get_by_role("button", name="Aggiungi criterio")

                # --- EDITOR: PERSONALIZZA HEADER E FOOTER ---
        self.btn_personalizza_header_footer = page.get_by_role("button", name="Personalizza Header e Footer")
        self.campo_titolo_report = page.get_by_role("textbox", name="Titolo Report")
        self.campo_sottotitolo = page.get_by_role("textbox", name="Sottotitolo")
        self.campo_url_logo = page.get_by_role("textbox", name="URL Logo personalizzato")
        self.select_allineamento_header = page.get_by_label("Allineamento Header", exact=True)
        self.campo_testo_footer = page.get_by_role("textbox", name="Testo Footer")
        self.checkbox_mostra_data_generazione = page.get_by_role("checkbox", name="Mostra data generazione")
        self.checkbox_mostra_numero_pagina = page.get_by_role("checkbox", name="Mostra numero pagina")
        self.input_aggiorna_preview = page.get_by_role("button", name="Aggiorna")

                # --- EDITOR: PREVIEW ---
        self.btn_aggiorna_preview = page.get_by_role("button", name="Aggiorna")
        self.btn_scarica_pdf_preview = page.get_by_role("button", name="Scarica PDF", exact=True)

        # --- MOD AGGIUNGI PARAMETRI ---
        self.btn_aggiungi_parametri = page.get_by_role("button", name="Aggiungi", exact=True)
        self.campo_filtrabile = (
            page.get_by_role("dialog")
            .locator(".v-autocomplete")
            .filter(has_text=re.compile(r"Campo filtrabile *"))
            .locator(".v-field__input")
        )
        self.btn_conferma_aggiungi_parametro = (
            page.get_by_role("dialog").get_by_role("button", name="Aggiungi", exact=True)
        )

        # --- LISTA TEMPLATE (pagina /reports) ---
        self.tab_miei_template = page.get_by_role("tab", name="I Miei Template")
        self.tab_template_globali = page.get_by_role("tab", name="Template Globali")
        self.campo_cerca_template = page.get_by_label("Cerca template...", exact=True)
        self.filtro_tipo_dataset = page.get_by_label("Tipo Dataset", exact=True)

# ============================================================
# NAVIGAZIONE
# ============================================================

    def apri_report(self):
        self.apri_gruppo_menu("Report & Analytics")
        self.naviga_a("/reports")

# ============================================================
# NUOVO REPORT — EDITOR
# ============================================================

    def seleziona_da_zero(self):
        self.bottone_crea_template.click()
        self.page.get_by_text("Da zero (editor)").click()

    def compila_impostazioni_template(self, dati: dict):
        """Compila la colonna 'Impostazioni Template' dell'editor report.

        :param dati: dict con chiavi nome_template, tipo_dataset (valore
                     tecnico enum, es. 'SALES_MASTER'), master_template,
                     descrizione — vedi ChainTestData.genera_dati_report_page()
        """
        self.campo_nome_template.fill(dati["nome_template"])

        etichetta_tipo = self.ETICHETTE_TIPO_DATASET.get(dati["tipo_dataset"], dati["tipo_dataset"])
        self.seleziona_option_per_testo_dropdown_icona(self.select_tipo_dataset_editor, etichetta_tipo)

        self.seleziona_option_per_testo_dropdown_icona(self.select_master_template, dati["master_template"])

        self.campo_descrizione_template.fill(dati["descrizione"])

    def compila_test_parametri(self, dati: dict):
        """Compila la sezione 'Test Parametri' dell'editor report.

        :param dati: dict con chiavi data_da, data_a (formato 'YYYY-MM-DD'),
                     granularita (valore tecnico 'day'/'week'/'month'),
                     limite_righe (int) — vedi ChainTestData.genera_dati_report_page()
        """
        self.compila_data(self.campo_data_da, dati["data_da"])
        self.compila_data(self.campo_data_a, dati["data_a"])

        etichetta_granularita = self.ETICHETTE_GRANULARITA.get(dati["granularita"], dati["granularita"])
        self.seleziona_option_per_testo_dropdown_icona(self.select_granularita, etichetta_granularita)

        self.campo_limite_righe.fill(str(dati["limite_righe"]))

    def compila_header_footer(self, dati: dict):
        """Apre il pannello 'Personalizza Header e Footer' e lo compila.

        :param dati: dict con chiavi titolo_report, sottotitolo, url_logo,
                     allineamento_header (valore tecnico 'left'/'center'/'right'),
                     testo_footer, mostra_data_generazione (bool),
                     mostra_numero_pagina (bool) — vedi
                     ChainTestData.genera_dati_report_page()
        """
        self.btn_personalizza_header_footer.click()

        self.campo_titolo_report.fill(dati["titolo_report"])
        self.campo_sottotitolo.fill(dati["sottotitolo"])
        self.campo_url_logo.fill(dati["url_logo"])

        etichetta_allineamento = self.ETICHETTE_ALLINEAMENTO_HEADER.get(
            dati["allineamento_header"], dati["allineamento_header"]
        )
        self.seleziona_option_per_testo_dropdown_icona(self.select_allineamento_header, etichetta_allineamento)

        self.campo_testo_footer.fill(dati["testo_footer"])

        # I checkbox riflettono lo stato desiderato invece di un click cieco:
        # 'Mostra data generazione' parte checked di default, 'Mostra numero
        # pagina' parte unchecked — set_checked gestisce entrambi i casi
        # senza doversi preoccupare dello stato iniziale.
        self.checkbox_mostra_data_generazione.set_checked(dati["mostra_data_generazione"])
        self.checkbox_mostra_numero_pagina.set_checked(dati["mostra_numero_pagina"])

    def apri_ordinamento_dati(self):
        """Clicca 'Aggiungi criterio'. NOTA: non conosco ancora cosa compare
        dopo (riga inline? dialog?) — da completare col prossimo dump/screenshot."""
        self.btn_aggiungi_criterio_ordinamento.click()

    def aggiorna_preview(self):
        self.btn_aggiorna_preview.click()
        # il bottone 'Scarica PDF' compare solo dopo che la preview è stata
        # generata: aspettarlo qui sincronizza il test con la generazione,
        # invece di affidarsi solo alla scomparsa di uno spinner
        expect(self.btn_scarica_pdf_preview).to_be_visible(timeout=30000)

    def scarica_pdf_preview(self, cartella_destinazione: str = "downloads") -> str:
        """Scarica il PDF generato dalla preview e restituisce il percorso
        locale del file, da usare per assert su esistenza/dimensione."""
        return self.clicca_e_scarica(self.btn_scarica_pdf_preview, cartella_destinazione)

# ============================================================
# MOD AGGIUNGI PARAMETRI
# ============================================================

    def apri_parametri(self):
        self.btn_aggiungi_parametri.click()
        expect(self.page.get_by_role("dialog")).to_be_visible()

    def seleziona_campo_casuale(self):
        self.page.get_by_text("Caricamento campi…").wait_for(state="hidden", timeout=10000)
        self.seleziona_option_casuale_dropdown_icona_in_modale(self.campo_filtrabile)

    def conferma_aggiungi_parametro(self):
        expect(self.btn_conferma_aggiungi_parametro).to_be_enabled(timeout=5000)
        self.btn_conferma_aggiungi_parametro.click()
        expect(self.page.get_by_role("dialog")).to_be_hidden()

# ============================================================
# LISTA TEMPLATE — TAB / RICERCA / FILTRO
# ============================================================

    def vai_a_tab_miei_template(self):
        self.tab_miei_template.click()

    def vai_a_tab_template_globali(self):
        self.tab_template_globali.click()

    def cerca_template(self, testo: str):
        self.campo_cerca_template.fill(testo)

    def filtra_per_tipo_dataset(self, tipo: str):
        etichetta = self.ETICHETTE_TIPO_DATASET.get(tipo, tipo)
        self.seleziona_option_per_testo_dropdown_icona(self.filtro_tipo_dataset, etichetta)

# ============================================================
# LISTA TEMPLATE — CARD SINGOLA
# ============================================================

    def _card_template(self, nome_template: str):
        return self.page.locator(".template-card").filter(has_text=nome_template)

    def _bottone_azione_card(self, nome_template: str, classe_icona: str):
        return self._card_template(nome_template).locator(f"button:has(.{classe_icona})")

    def nome_primo_template_visibile(self) -> str:
        primo = self.page.locator(".template-card").first
        primo.wait_for(state="visible")
        return primo.locator(".v-card-title .text-truncate").inner_text()

    def preview_html_template(self, nome_template: str):
        self._bottone_azione_card(nome_template, "mdi-eye").click()

    def chiudi_preview_html(self):
        dialog = self.page.get_by_role("dialog")
        dialog.get_by_role("button", name="Chiudi", exact=True).click()
        dialog.wait_for(state="hidden")

    def scarica_pdf_template(self, nome_template: str, cartella_destinazione: str = "downloads"):
        return self.clicca_e_scarica(
            self._bottone_azione_card(nome_template, "mdi-file-pdf-box"), cartella_destinazione
        )

    def scarica_excel_template(self, nome_template: str, cartella_destinazione: str = "downloads"):
        return self.clicca_e_scarica(
            self._bottone_azione_card(nome_template, "mdi-file-excel"), cartella_destinazione
        )

    def modifica_template(self, nome_template: str):
        self._bottone_azione_card(nome_template, "mdi-pencil").click()

    def duplica_template(self, nome_template: str):
        self._bottone_azione_card(nome_template, "mdi-content-copy").click()

    def esporta_json_template(self, nome_template: str, cartella_destinazione: str = "downloads"):
        return self.clicca_e_scarica(
            self._bottone_azione_card(nome_template, "mdi-download"), cartella_destinazione
        )

    def elimina_template(self, nome_template: str):
        self._bottone_azione_card(nome_template, "mdi-delete").click()
        self.page.get_by_role("dialog").get_by_role("button", name="Elimina", exact=True).click()