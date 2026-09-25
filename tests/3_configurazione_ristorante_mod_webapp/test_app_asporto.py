import pytest
from pages.mod_3_configurazione_ristorante_mod_webapp.App_Asporto_ServiziPage import AppAsportoPage
from utils.test_data import ChainTestData

class TestAppAsportoServizi:
    def test_apre_pagina_servizi(self,authenticated_page):
        servizi = AppAsportoPage(authenticated_page)
        servizi.apri_app_asporto_servizi()

        # --- COMPILA MODULO APP BRANDING ---
        servizi.seleziona_tema_random()
        dati_social = ChainTestData.genera_dati_app_asporto()
        servizi.compila_social_mod(dati_social)

        # --- COMPILA TAB TESTI ---
        servizi.seleziona_tab_testi()
        dati_testi = ChainTestData.genera_dati_app_asporto_tab_testi()
        servizi.compila_tab_testi(dati_testi)

        # --- COMPILA TAB LOGHI E IMMAGINI ---
        servizi.click_doppio_btn()
        dati_loghi = ChainTestData.genera_dati_app_asporto_tab_loghi_e_immagini()
        servizi.compila_tab_loghi_e_immagini(dati_loghi)






# per avviare il test: - pytest tests/3_configurazione_ristorante_mod_webapp/test_app_asporto.py --headed
# per avviare il test di tutta la cartella configurazione ristorante mod webapp: - pytest tests/3_configurazione_ristorante_mod_webapp
# per aprire il report finale: - start reports\report.html