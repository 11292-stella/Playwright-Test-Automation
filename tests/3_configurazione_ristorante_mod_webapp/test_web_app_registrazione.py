from pages.mod_3_configurazione_ristorante_mod_webapp.Web_app_registrazionePage import WebAppRegistrazione
from utils.test_data import ChainTestData

class TestWebAppRegistrazione:
    def test_web_app_registrazione(self,authenticated_page):
        rec = WebAppRegistrazione(authenticated_page)
        rec.apri_app_registrazione()

        rec.seleziona_tema_random()

        rec.vai_a_testi()

        dati_testi = ChainTestData.genera_dati_registrazione_testi()
        rec.compila_testi(dati_testi)

        rec.vai_a_immagini()
        rec.seleziona_tutte_le_immagini()

        rec.vai_a_verifica()
        rec.seleziona_metodo_verifica_random()

        rec.vai_a_campi_form()
        rec.configura_campi_form_random()

        rec.vai_a_privacy()
        rec.usa_mod_base()

        rec.vai_a_hand_off()
        rec.mostra_qr()

        rec.vai_a_stampa_qr()
        dati_qr = ChainTestData.genera_dati_stampa_qr()
        rec.stampa_qr(dati_qr)
        rec.seleziona_formato_stampa_random()
        


# per avviare tutti: pytest tests/3_configurazione_ristorante_mod_webapp/test_web_app_registrazione.py --headed