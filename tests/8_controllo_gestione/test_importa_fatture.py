from pages.mod_8_controllo_gestione.ImportaFatturePage import ImportFatture
from utils.test_data import ChainTestData

class TestImportFatture:
    def test_import(self,authenticated_page):
        importa = ImportFatture(authenticated_page)
        importa.apri_import_fatture()

        percorso_file = ChainTestData.genera_percorso_fattura_test()
        importa.carica_fattura(percorso_file)
        importa.completa_mapping_articoli()

# per avviare il test: - pytest tests/8_controllo_gestione/test_importa_fatture.py --headed
# per avviare il test di tutta la cartella: - pytest tests/8_controllo_gestione
# per aprire il report finale: - start reports\report.html