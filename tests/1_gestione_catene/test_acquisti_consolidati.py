from pages.mod_1_gestione_catene.Acquisti_Consolidati_Page import AcquistiPage


class TestAcquisti:

    def test_filtro_catena_acquisti(self, authenticated_page):
        acquisti = AcquistiPage(authenticated_page)
        acquisti.apri_acquisti()
        acquisti.filtra_per_catena("Catena_Test (demo_catena_test)")
        acquisti.click_fabbisogno()






# per avviare il test: - pytest tests/1_gestione_catene/test_acquisti_consolidati.py --headed
# per avviare il test di tutta la cartella gestione_catene: - pytest tests/1_gestione_catene
# per aprire il report finale: - start reports\report.html 