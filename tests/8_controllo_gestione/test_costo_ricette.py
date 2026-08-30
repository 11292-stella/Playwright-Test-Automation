from pages.mod_8_controllo_gestione.CostoRicettePage import CostoRicette

class TestCostoRicette:
    def test_costo_ricette(self,authenticated_page):
        costo = CostoRicette(authenticated_page)
        costo.apri_costo_ricette()

        costo.selezione_random_costo()
        costo.genera_dati_costo()
        costo.ricalcola_costo()



# per avviare il test: - pytest tests/8_controllo_gestione/test_costo_ricette.py --headed
# per avviare il test di tutta la cartella: - pytest tests/8_controllo_gestione
# per aprire il report finale: - start reports\report.html