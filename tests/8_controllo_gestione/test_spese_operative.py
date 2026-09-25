from pages.mod_8_controllo_gestione.SpeseOperativePage import SpeseOperative
from utils.test_data import ChainTestData

class TestSpeseOperative:
    def test_spese(self,authenticated_page):
        spese = SpeseOperative(authenticated_page)
        spese.apri_spese_operative()

        dati = ChainTestData.genera_dati_nuova_spesa_operativa()
        spese.compila_nuova_spesa(dati)







# per avviare il test: - pytest tests/8_controllo_gestione/test_spese_operative.py --headed
# per avviare il test di tutta la cartella: - pytest tests/8_controllo_gestione
# per aprire il report finale: - start reports\report.html