from pages.mod_6_fidelity.Carte_FidelityPage import CarteFidelity, expect
from utils.test_data import ChainTestData

class TestFidelity:
    def test_fidelity(self,authenticated_page):
        fidelity = CarteFidelity(authenticated_page)
        fidelity.apri_carte_fidelity()

        fidelity.crea_nuova_carta()
        dati_mod = ChainTestData.genera_dati_carta_fidelity()
        fidelity.compila_barcode(dati_mod)
        fidelity.cerca_e_seleziona_cliente(dati_mod["cliente"])
        fidelity.elenca_dropdown_pagina(".v-select")
        fidelity.seleziona_tier_casuale()
        fidelity.seleziona_listino_casuale()

        



# per avviare il test: - pytest tests/6_fidelity/test_carte_fidelity.py --headed
# per avviare il test di tutta la cartella gestione_catene: - pytest tests/6_fidelity
# per aprire il report finale: - start reports\report.html