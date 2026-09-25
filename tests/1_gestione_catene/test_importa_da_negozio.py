from playwright.sync_api import expect
from pages.mod_1_gestione_catene.Importa_da_negozioPage import ImportaDA
from utils.test_data import ChainTestData

class TestImporta:
    def test_importa(self,authenticated_page):
        importa = ImportaDA(authenticated_page)
        importa.apri_catalogo()
        importa.filtra_per_catena("Catena_Test (demo_catena_test)")

        importa.cerca_negozio("Ristorante Demo")
        importa.deseleziona_tutte_le_sezioni()
        importa.seleziona_sezione_casuale()
        importa.click_analizza_anteprima()
        importa.controlla_e_importa() 





# per avviare il test: pytest tests/1_gestione_catene/test_importa_da_negozio.py --headed