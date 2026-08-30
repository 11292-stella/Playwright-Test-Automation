from pages.mod_4_email_marketing.CampagnePage import CampagneMarketing
from utils.test_data import ChainTestData

class TestCampagneMarketing:
    def test_campagne_marketing(self,authenticated_page):
        marketing = CampagneMarketing(authenticated_page)
        marketing.apri_campagne_marketing()

        marketing.crea_nuova_campagna()

        dati_modulo = ChainTestData.genera_dati_nuova_campagna()
        marketing.compila_mod_campagana(dati_modulo)
        marketing.seleziona_primo_segmento_destinatari()
        marketing.compila_secondo_modale(dati_modulo)

        # --- TAB ANTEPRIMA ---
        marketing.vai_a_anteprima()
        marketing.visualizza_tutte_anteprime()

        # --- PROVA INVIO ---
        marketing.click_invio_prova()

        # --- PROVA PROGRAMMA --
        dati_programma = ChainTestData.genera_dati_programma_ora_e_data()
        marketing.click_programma(dati_programma)



# per avviare il test: - pytest tests/4_email_marketing/test_campagne_marketing.py --headed
# per avviare il test di tutta la cartella gestione_catene: - pytest tests/4_email_marketing
# per aprire il report finale: - start reports\report.html