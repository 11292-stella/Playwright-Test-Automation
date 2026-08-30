from playwright.async_api import expect
from pages.mod_0_stabilita_moduli_cypress.Ddt_Tabacchi_Page import DdtTabacchi
from utils.test_data import ChainTestData

class TestDdtTabacchi:
    def test_creazione_e_conferma_ddt_da_ordine(self, authenticated_page):
        ddt = DdtTabacchi(authenticated_page)
        ddt.apri_catalogo_tabacchi_ddt()

        # --- NUOVO DDT DA ORDINE (scenario che crashava in Cypress: flusso completo) ---
        ddt.apri_modale_nuovo_ddt_da_ordine()

        ddt.cerca_e_seleziona_ordine("TAB260706-007 — Dickens-Davis")

        




# per avviare il test: - pytest tests/0_stabilita_moduli_cypress/test_ddt_tabacchi.py --headed
# per avviare il test di tutta la cartella stabilita moduli cypress: - pytest tests/0_stabilita_moduli_cypress
# per aprire il report finale: - start reports\report.html