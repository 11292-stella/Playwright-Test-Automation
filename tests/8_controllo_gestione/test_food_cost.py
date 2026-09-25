from pages.mod_8_controllo_gestione.FoodCostPage import FoodCost

class TestFoodCost:
    def test_food_cost(self,authenticated_page):
        cost = FoodCost(authenticated_page)
        cost.apri_food_cost()
        
        
        

        cost.seleziona_da_drop()
        cost.genera_dati_e_aggiorna()
        cost.visualizza()


# per avviare il test: - pytest tests/8_controllo_gestione/test_food_cost.py --headed
# per avviare il test di tutta la cartella: - pytest tests/8_controllo_gestione
# per aprire il report finale: - start reports\report.html