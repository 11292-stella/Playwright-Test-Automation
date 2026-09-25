from pages.mod_8_controllo_gestione.SprechiPage import Sprechi
from utils.test_data import ChainTestData

class TestSprechi:
    def test_sprechi(self,authenticated_page):
        sprechi = Sprechi(authenticated_page)
        sprechi.apri_sprechi()

        sprechi.apri_nuovo_spreco()
        dati_spreco = ChainTestData.genera_dati_nuovo_spreco()
        sprechi.compila_modale_spreco("Basilico Fresco 0080", dati_spreco)
        sprechi.elimina_registrazione("Basilico Fresco 0080")

# per avviare il test: - pytest tests/8_controllo_gestione/test_sprechi.py --headed
# per avviare il test di tutta la cartella: - pytest tests/8_controllo_gestione
# per aprire il report finale: - start reports\report.html
