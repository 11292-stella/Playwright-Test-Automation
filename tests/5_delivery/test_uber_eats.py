from pages.mod_5_delivery.UberEatsPage import UberEats
from utils.test_data import ChainTestData


class TestUberEats:

    def test_configurazione_uber_eats(self, authenticated_page):
        uber_eats = UberEats(authenticated_page)
        uber_eats.apri_provider()

        uber_eats.abilita_provider()
        dati_uber_eats = ChainTestData.genera_dati_uber_eats()
        uber_eats.compila_id(dati_uber_eats)
        uber_eats.compila_campi_comuni(dati_uber_eats)
        uber_eats.abilita_switch_accetta()
        uber_eats.salva_configurazione()

    def test_creazione_categoria_menu_uber_eats(self, authenticated_page):
        uber_eats = UberEats(authenticated_page)
        uber_eats.apri_provider()
        uber_eats.vai_a_menu()

        uber_eats.crea_nuova_categoria()
        uber_eats.dropdown_importa("Bevande UNISCI")
        uber_eats.aggiungi_img_categoria()

        # cleanup
        uber_eats.rimuovi_prodotti_ed_elimina_ultima_categoria()


# per avviare il test: - pytest tests/5_delivery/test_uber_eats.py --headed
# per avviare il test di tutta la cartella gestione_catene: - pytest tests/5_delivery
# per aprire il report finale: - start reports\report.html
