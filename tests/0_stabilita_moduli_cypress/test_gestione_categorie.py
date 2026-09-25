from playwright.async_api import expect
from pages.mod_0_stabilita_moduli_cypress.Gestione_Categorie_Page import GestioneCat
from utils.test_data import ChainTestData

class TestGestione:
    def test_gestione(self,authenticated_page):
        gestione = GestioneCat(authenticated_page)
        gestione.apri_catalogo()

        # --- NUOVA CATEGORIA ---
        gestione.apri_modale_categoria()

        dati_categoria = ChainTestData.genera_dati_categorie_prodotto()
        gestione.compila_categoria(dati_categoria)

        # --- CATEGORIA PADRE (punto che crashava in Cypress) ---
        gestione.seleziona_categoria_padre_casuale()

        gestione.crea_categoria()

        gestione.compila_modulo_post(dati_categoria)


# per avviare il test: pytest tests/0_stabilita_moduli_cypress/test_gestione_categorie.py --headed