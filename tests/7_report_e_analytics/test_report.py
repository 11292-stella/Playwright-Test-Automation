from pages.mod_7_report_e_analytics.ReportPages import Report
from utils.test_data import ChainTestData
import os


class TestReport:
    def test_report(self, authenticated_page):
        report = Report(authenticated_page)
        report.apri_report()

        # --- NUOVO REPORT DA ZERO ---
        report.seleziona_da_zero()

        dati = ChainTestData.genera_dati_report_page()
        report.compila_impostazioni_template(dati)
        report.compila_test_parametri(dati)
        report.compila_header_footer(dati)

        report.apri_parametri()
        report.seleziona_campo_casuale()
        report.conferma_aggiungi_parametro()

        # --- PREVIEW E DOWNLOAD PDF ---
        report.aggiorna_preview()
        percorso_pdf = report.scarica_pdf_preview()

        assert os.path.exists(percorso_pdf), f"File non trovato: {percorso_pdf}"
        assert percorso_pdf.lower().endswith(".pdf"), f"Estensione inattesa: {percorso_pdf}"
        assert os.path.getsize(percorso_pdf) > 0, "Il PDF scaricato è vuoto (0 byte)"


class TestReportLista:
    def test_ricerca_filtro_e_azioni_su_template(self, authenticated_page):
        report = Report(authenticated_page)
        report.apri_report()

        report.vai_a_tab_template_globali()
        report.vai_a_tab_miei_template()
        report.salva_html_pagina("report tab template_globali")

        report.cerca_template("test")
        report.cerca_template("")
        report.filtra_per_tipo_dataset("SALES_MASTER")

        nome = report.nome_primo_template_visibile()
        report.preview_html_template(nome)
        report.chiudi_preview_html()
        report.scarica_pdf_template(nome)


# per avviare il test: - pytest tests/7_report_e_analytics/test_report.py --headed
# per avviare solo la creazione: - pytest tests/7_report_e_analytics/test_report.py::TestReport --headed
# per avviare solo lista/filtri: - pytest tests/7_report_e_analytics/test_report.py::TestReportLista --headed
# per avviare il test di tutta la cartella: - pytest tests/7_report_e_analytics
# per aprire il report finale: - start reports\report.html