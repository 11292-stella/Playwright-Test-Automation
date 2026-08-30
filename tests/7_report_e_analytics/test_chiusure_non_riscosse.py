from pages.mod_7_report_e_analytics.ChiusureNonRiscossePage import Chiusure

class TestChiusure:
    def test_chiusure_non_riscosse(self,authenticated_page):
        chiusure = Chiusure(authenticated_page)
        chiusure.apri_chiusure_non_riscosse()
       

        # --- TAB AUTOCONSUMO TITOLARE ---
        chiusure.aggiorna_anteprima()

        # --- TAB PASTI DIPENDENTI ---
        chiusure.vai_a_tab_pasti_dipendenti()
        
        
        # --- TAB ADDESTRAMENTO ---
        chiusure.vai_a_tab_addestramento()
        
        
        # --- TAB REPORT GENERATI ---
        chiusure.vai_a_tab_report()
        


# per avviare il test: - pytest tests/7_report_e_analytics/test_chiusure_non_riscosse.py --headed
# per avviare il test di tutta la cartella: - pytest tests/7_report_e_analytics
# per aprire il report finale: - start reports\report.html