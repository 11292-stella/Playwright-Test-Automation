from pages.mod_8_controllo_gestione.CategorieCostoPage import CategorieCosto
from utils.test_data import ChainTestData

class TestCategorieCosto:
    def test_categorie_costo(self,authenticated_page):
        costo = CategorieCosto(authenticated_page)
        costo.apri_categorie_costo()

        dati_categoria = ChainTestData.genera_dati_nuova_categoria_costo()
        costo.compila_mod(dati_categoria)


# per avviare il test: - pytest tests/8_controllo_gestione/test_categorie_costo.py --headed
# per avviare il test di tutta la cartella: - pytest tests/8_controllo_gestione
# per aprire il report finale: - start reports\report.html