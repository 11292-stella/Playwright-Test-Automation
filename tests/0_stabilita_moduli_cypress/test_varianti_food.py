from playwright.async_api import expect
from pages.mod_0_stabilita_moduli_cypress.Varianti_Food_Page import Varianti

class TestVarianti:
    def test_varianti(self,authenticated_page):
        varianti = Varianti(authenticated_page)
        varianti.apri_catalogo()
        varianti.apri_modale_prodotto()

        # --- CERCA E SELEZIONA GRUPPO ---
        varianti.cerca_e_seleziona_gruppo("Gruppo Bespoke 34AK")





# per avviare il test: pytest tests/0_stabilita_moduli_cypress/test_varianti_food.py --headed