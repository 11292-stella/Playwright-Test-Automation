from playwright.sync_api import expect
from pages.mod_7_report_e_analytics.SchedulazioniPage import Schedulazioni
from utils.test_data import ChainTestData


class TestSchedulazioni:
    def test_nuova_schedulazione(self, authenticated_page):
        schede = Schedulazioni(authenticated_page)
        schede.apri_schedulazioni()
        schede.apri_nuova_schedulazione()

        dati = ChainTestData.genera_dati_schedulazione_nuova()
        schede.compila_nuova_schedulazione(dati)

        expect(schede.btn_crea).to_be_enabled()
        schede.btn_crea.click()

        expect(schede.page.get_by_role("dialog")).to_be_hidden()
        expect(schede.page.get_by_text(dati["nome"], exact=True)).to_be_visible()
        

       


# per avviare il test: - pytest tests/7_report_e_analytics/test_schedulazioni.py --headed


# per avviare il test: - pytest tests/7_report_e_analytics/test_schedulazioni.py --headed
# per avviare il test di tutta la cartella: - pytest tests/7_report_e_analytics
# per aprire il report finale: - start reports\report.html