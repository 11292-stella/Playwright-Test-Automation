from pages.mod_5_delivery.DeliverectPage import Deliverect
from utils.test_data import ChainTestData


class TestDeliverect:

    def test_configurazione_deliverect(self, authenticated_page):
        deliverect = Deliverect(authenticated_page)
        deliverect.apri_provider()

        deliverect.abilita_provider()
        dati_deliverect = ChainTestData.genera_dati_deliverect()
        deliverect.compila_id(dati_deliverect)
        deliverect.compila_campi_comuni(dati_deliverect)
        deliverect.abilita_switch_accetta()
        deliverect.salva_configurazione()

    def test_creazione_categoria_menu_deliverect(self, authenticated_page):
        deliverect = Deliverect(authenticated_page)
        deliverect.apri_provider()
        deliverect.vai_a_menu()

        deliverect.crea_nuova_categoria()
        deliverect.dropdown_importa("Bevande UNISCI")
        deliverect.aggiungi_img_categoria()

        # cleanup
        deliverect.rimuovi_prodotti_ed_elimina_ultima_categoria()


# per avviare il test: - pytest tests/5_delivery/test_deliverect.py --headed
# per avviare il test di tutta la cartella gestione_catene: - pytest tests/5_delivery
# per aprire il report finale: - start reports\report.html
