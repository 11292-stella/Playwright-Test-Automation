from pages.mod_5_delivery.DeliverooPage import Deliveroo,expect
from utils.test_data import ChainTestData

class TestDeliveroo:
    def test_deliveroo(self,authenticated_page):
        deliveroo = Deliveroo(authenticated_page)
        deliveroo.apri_delivery()

        deliveroo.abilita_deliveroo()
        deliveroo.abilita_switch_accetta()
        dati_deliveroo = ChainTestData.genera_dati_deliveroo()
        deliveroo.compila_modulo_deliveroo(dati_deliveroo)
        deliveroo.salva_configurazione()

        # --- TAB MENU ---
        deliveroo.vai_a_menu()
        deliveroo.crea_nuova_categoria()
        deliveroo.dropdown_importa("Bevande UNISCI")
        deliveroo.aggiungi_img_categoria()
        deliveroo.rimuovi_prodotti_ed_elimina_ultima_categoria()
        

    def test_verifica_senza_credenziali(self, authenticated_page):
        deliveroo = Deliveroo(authenticated_page)
        deliveroo.apri_delivery()
        deliveroo.abilita_deliveroo()
        dati_id = ChainTestData.genera_dati_deliveroo()
        deliveroo.compila_solo_id(dati_id)
        expect(deliveroo.page.get_by_text("Credenziali Deliveroo mancanti")).to_be_visible()


# per avviare il test: - pytest tests/5_delivery/test_deliveroo.py --headed
# per avviare il test di tutta la cartella gestione_catene: - pytest tests/5_delivery
# per aprire il report finale: - start reports\report.html