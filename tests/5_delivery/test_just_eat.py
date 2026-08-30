from pages.mod_5_delivery.JustEatPage import JustEat
from utils.test_data import ChainTestData


class TestJustEat:

    def test_configurazione_just_eat(self, authenticated_page):
        just_eat = JustEat(authenticated_page)
        just_eat.apri_provider()

        just_eat.abilita_provider()
        dati_just_eat = ChainTestData.genera_dati_just_eat()
        just_eat.compila_id(dati_just_eat)
        just_eat.compila_campi_comuni(dati_just_eat)
        just_eat.abilita_switch_accetta()
        just_eat.salva_configurazione()

    def test_creazione_categoria_menu_just_eat(self, authenticated_page):
        just_eat = JustEat(authenticated_page)
        just_eat.apri_provider()
        just_eat.vai_a_menu()

        just_eat.crea_nuova_categoria()
        just_eat.dropdown_importa("Bevande UNISCI")
        just_eat.aggiungi_img_categoria()

        # cleanup
        just_eat.rimuovi_prodotti_ed_elimina_ultima_categoria()


# per avviare il test: - pytest tests/5_delivery/test_just_eat.py --headed
# per avviare il test di tutta la cartella gestione_catene: - pytest tests/5_delivery
# per aprire il report finale: - start reports\report.html
