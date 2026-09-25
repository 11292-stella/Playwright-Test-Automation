from playwright.sync_api import Page
from pages.mod_1_gestione_catene.chain_page import ChainPage
from utils.test_data import ChainTestData


def test_creazione_ed_eliminazione_catena(authenticated_page: Page):
    chain_page = ChainPage(authenticated_page)
    dati_faker = ChainTestData.genera_dati_nuova_catena()
    
    # 1. Navigazione
    chain_page.apri_modulo_catene()
    
    # 2. Creazione nuova catena
    chain_page.apri_form_nuova_catena()
    chain_page.compila_form_catena(dati_faker)
    
    # 3. Pulizia: Eliminazione della catena appena creata
    chain_page.elimina_catena(dati_faker["nome"])

    # per avviare il test:  pytest tests/1_gestione_catene/test_chains.py --headed