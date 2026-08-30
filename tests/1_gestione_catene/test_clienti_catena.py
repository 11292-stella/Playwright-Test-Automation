from playwright.sync_api import expect
from pages.mod_1_gestione_catene.Catena_clientiPage import ClientiPage


class TestClienti:
    def test_toggle_crm_catena_persiste_dopo_reload(self, authenticated_page):
        clienti = ClientiPage(authenticated_page)
        clienti.apri_clienti()
        clienti.filtra_per_catena("Catena Demo (reseller_demo_catena_demo)")
        clienti.attiva_e_salva_crm_catena()

        authenticated_page.reload()
        clienti.attendi_scomparsa_loader()

        expect(clienti.toggle_catena).to_be_checked()
        expect(clienti.banner_non_abilitato).not_to_be_visible()


# per avviare il test: pytest tests/1_gestione_catene/test_clienti_catena.py --headed