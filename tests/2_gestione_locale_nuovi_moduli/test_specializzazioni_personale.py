from playwright.sync_api import expect
from pages.mod_2_gestione_locale_nuovi_moduli.Specializzazioni_personalePage import SpecializzazioniPersonalePage
from utils.test_data import ChainTestData

class TestSpecializzazioniPersonale:
    def test_apertura_pagina(self, authenticated_page):
        pagina = SpecializzazioniPersonalePage(authenticated_page)
        pagina.apri_specializzazioni_personale()

        # --- NUOVA SPECIALIZZAZIONE ---
        pagina.crea_nuova_specializzazione()
        dati_specializzazione = ChainTestData.genera_dati_specializzazione_personale()
        pagina.compila_modulo_specializzazione(dati_specializzazione)

        # --- MODULO OPERATORI ---
        pagina.click_vai_a_operatori()
        dati_operatore = ChainTestData.genera_dati_nuovo_operatore_con_specializzazione()
        pagina.crea_e_compila_nuovo_operatore_con_specializzazione(dati_operatore)
        pagina.espandi_profilo_servizi_appuntamento()
        pagina.seleziona_specializzazioni(["Cucina Vegana", "Pasticcere", "Sommelier"])

        dati_mod = ChainTestData.genera_dati_mod_successivo()
        pagina.click_e_completa_dopo_switch(dati_mod)



# per avviare il test: pytest tests/2_gestione_locale_nuovi_moduli/test_specializzazioni_personale.py --headed