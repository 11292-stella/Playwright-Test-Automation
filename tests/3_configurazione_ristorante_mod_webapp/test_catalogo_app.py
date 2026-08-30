from pages.mod_3_configurazione_ristorante_mod_webapp.Catalogo_AppPage import CatalogoApp
from utils.test_data import ChainTestData

class TestCatalogoAsporto:
    def test_catalogo_app(self,authenticated_page):
        catalogo = CatalogoApp(authenticated_page)
        catalogo.apri_app_catalogo()

        catalogo.seleziona_categoria("Bevande UNISCI")

        # --- MENU APP ---
        catalogo.apri_tab_menu()
        dati_menu = ChainTestData.genera_dati_catalogo_app()
        catalogo.compila_nuovo_menu(dati_menu)

        catalogo.seleziona_giorno_random()
        date = ChainTestData.genera_dati_date_disponibilita()
        catalogo.compila_date_disponibilita(date["data_inizio"], date["data_fine"])


# per avviare tutti: pytest tests/3_configurazione_ristorante_mod_webapp/test_catalogo_app.py --headed