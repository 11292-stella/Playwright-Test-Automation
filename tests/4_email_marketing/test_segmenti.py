from pages.mod_4_email_marketing.SegmentiPage import Segmenti
from utils.test_data import ChainTestData

class TestSegmenti:
    def test_segmenti(self,authenticated_page):
        segmenti = Segmenti(authenticated_page)
        segmenti.apri_segmenti()

        segmenti.crea_nuovo_segmento()

        segmenti.seleziona_tipo_random()

        segmenti.seleziona_mese_compleanno_random()

        segmenti.selezione_lingua_random()

        dati_segmento = ChainTestData.genera_dati_nuovo_segmento()
        segmenti.compila_mod_nuovo_segmento(dati_segmento)

        



# per avviare il test: - pytest tests/4_email_marketing/test_segmenti.py --headed
# per avviare il test di tutta la cartella gestione_catene: - pytest tests/4_email_marketing
# per aprire il report finale: - start reports\report.html