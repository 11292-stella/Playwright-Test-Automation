from pages.mod_5_delivery.GlovoPage import Glovo
from utils.test_data import ChainTestData


class TestGlovo:

    def test_configurazione_glovo(self, authenticated_page):
        glovo = Glovo(authenticated_page)
        glovo.apri_provider()

        glovo.abilita_provider()
        dati_glovo = ChainTestData.genera_dati_glovo()
        glovo.compila_id(dati_glovo)
        glovo.compila_campi_comuni(dati_glovo)
        glovo.abilita_switch_accetta()
        glovo.salva_configurazione()

    def test_creazione_categoria_menu_glovo(self, authenticated_page):
        glovo = Glovo(authenticated_page)
        glovo.apri_provider()
        glovo.vai_a_menu()

        glovo.crea_nuova_categoria()
        glovo.dropdown_importa("Bevande UNISCI")
        glovo.aggiungi_img_categoria()

        # cleanup
        glovo.rimuovi_prodotti_ed_elimina_ultima_categoria()


# per avviare il test: - pytest tests/5_delivery/test_glovo.py --headed
# per avviare il test di tutta la cartella gestione_catene: - pytest tests/5_delivery
# per aprire il report finale: - start reports\report.html
