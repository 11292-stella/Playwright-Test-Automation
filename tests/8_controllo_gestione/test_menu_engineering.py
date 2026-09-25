from pages.mod_8_controllo_gestione.MenuEngineeringPage import MenuEngineering

class TestMenu:
    def test_menu(self,authenticated_page):
        menu = MenuEngineering(authenticated_page)
        menu.apri_menu_engineering()

        menu.seleziona_da_drop()
        menu.genera_dati_e_aggiorna()

# per avviare il test: - pytest tests/8_controllo_gestione/test_menu_engineering.py --headed
# per avviare il test di tutta la cartella: - pytest tests/8_controllo_gestione
# per aprire il report finale: - start reports\report.html