from playwright.async_api import expect
from pages.mod_0_stabilita_moduli_cypress.Fornitori_Page import Fornitori
from utils.test_data import ChainTestData

class TestFornitori:
    def test_fornitori(self,authenticated_page):
        fornitori = Fornitori(authenticated_page)
        fornitori.apri_catalogo()
        fornitori.seleziona_acquistabili()
        fornitori.cerca_e_seleziona_tab_fornitori()

        # --- CERCA E SELEZIONA FORNITORE ---
        fornitori.cerca_e_seleziona_fornitore("Abernathy - Swift")

        # --- COMPILA MOD ---
        dati_fornitore = ChainTestData.genera_dati_nuovo_fornitore_prodotto()
        
        fornitori.compila_mod_fornitore(dati_fornitore)

        
        fornitori.compila_mod_sotto(dati_fornitore)
        

       
        




# per avviare il test: pytest tests/0_stabilita_moduli_cypress/test_fornitori.py --headed