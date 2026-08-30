from playwright.async_api import expect
from pages.mod_0_stabilita_moduli_cypress.Ricetta_Page import Ricetta
from utils.test_data import ChainTestData

class TestRicetta:
    def test_ricetta(self,authenticated_page):
        ricetta = Ricetta(authenticated_page)
        ricetta.apri_catalogo()

        # --- NUOVO PRODOTTO ---
        ricetta.apri_modale_prodotto()
        ricetta.tab_ricetta()

        # --- SELEZIONE INGREDIENTE (punto che crashava in Cypress) ---
        ricetta.cerca_e_seleziona_ingrediente("Burro 4648")
        dati_ingrediente = ChainTestData.genera_dati_nuova_ricetta_prodotto()
        ricetta.compila_dati_ingrediente_selezionato(dati_ingrediente)
        ricetta.compila_modulo_sottostante_ricetta(dati_ingrediente)


# per avviare il test: pytest tests/0_stabilita_moduli_cypress/test_ricetta.py --headed

