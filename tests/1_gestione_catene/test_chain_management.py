from playwright.sync_api import Page
from pages.mod_1_gestione_catene.chain_page import ChainPage
from utils.test_data import ChainTestData


def test_associazione_negozio_pane_e_burro(authenticated_page: Page):
    chain_page = ChainPage(authenticated_page)
    chain_page.apri_modulo_catene()

    # Catena "usa e getta": creata fresca ad ogni run, cosi il nome e
    # sempre noto e non c'e stato da pulire tra un run e l'altro.
    dati_catena = ChainTestData.genera_dati_nuova_catena()
    chain_page.apri_form_nuova_catena()
    chain_page.compila_form_catena(dati_catena)
    chain_page.attendi_scomparsa_loader()

    NEGOZIO_TARGET = "Ristorante Demo"

    # 1. Apertura modale gestione negozi della catena appena creata
    chain_page.apri_gestione_negozi(dati_catena["nome"])

    # 2. Associazione negozio
    chain_page.associa_negozio_a_catena(NEGOZIO_TARGET)

    # 3. Assertion: verifica la corretta presenza nella lista
    chain_page.verifica_negozio_associato(NEGOZIO_TARGET)

    # 4. Pulizia: il negozio va rimosso PRIMA di chiudere/eliminare la
    # catena, altrimenti l'eliminazione fallisce ("solo se priva di negozi")
    chain_page.rimuovi_negozio_se_presente(NEGOZIO_TARGET)
    chain_page.chiudi_modale_negozi()

    # 5. Eliminazione della catena di test
    chain_page.elimina_catena(dati_catena["nome"])

    # per avviare il test: pytest tests/1_gestione_catene/test_chain_management.py --headed
