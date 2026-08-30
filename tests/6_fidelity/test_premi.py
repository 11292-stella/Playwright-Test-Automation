from pages.mod_6_fidelity.PremiPage import Premi
from utils.test_data import ChainTestData

class TestPremi:
 
    # --- TIPO PREMIO: SCONTO ---
 
    def test_premi_con_sconto(self, authenticated_page):
        premi = Premi(authenticated_page)
        premi.apri_premi()
 
        premi.abilita_switch()
 
        premi.crea_nuovo_premio()
        dati_premio = ChainTestData.genera_dati_premio()
        premi.compila_premio(dati_premio)
        premi.seleziona_tipo_sconto_casuale()
        premi.seleziona_tier_casuale()
 
    # --- TIPO PREMIO: PRODOTTO GRATIS ---
 
    def test_premi_con_prodotto_gratis(self, authenticated_page):
        premi = Premi(authenticated_page)
        premi.apri_premi()
    
        premi.abilita_switch()
    
        premi.crea_nuovo_premio()
        dati_premio = ChainTestData.genera_dati_premio()
        premi.compila_premio(dati_premio)
        premi.seleziona_tipo_prodotto_gratis()
        premi.cerca_e_seleziona_prodotto_gratis("Pollo alla Cacciatora")
        premi.seleziona_tier_casuale()
 
    # --- TIPO PREMIO: CREDITO ---
 
    def test_premi_con_credito(self, authenticated_page):
        premi = Premi(authenticated_page)
        premi.apri_premi()
    
        premi.abilita_switch()
    
        premi.crea_nuovo_premio()
        dati_premio = ChainTestData.genera_dati_premio()
        premi.seleziona_credito()
        premi.compila_mod_con_credito(dati_premio)
        premi.seleziona_tier_casuale()
 
    # --- TIPO PREMIO: COUPON ---
 
    def test_premi_con_coupon(self, authenticated_page):
        premi = Premi(authenticated_page)
        premi.apri_premi()
 
        premi.abilita_switch()
 
        premi.crea_nuovo_premio()
        dati_premio = ChainTestData.genera_dati_premio_con_prodotti_gratis()
        premi.seleziona_coupon()
        premi.compila_mod_coupon(dati_premio)
        premi.seleziona_tipo_coupon_casuale()
        premi.seleziona_tier_casuale()
            
    



# per avviare il test: - pytest tests/6_fidelity/test_premi.py --headed
# per avviare il test di tutta la cartella gestione_catene: - pytest tests/6_fidelity
# per aprire il report finale: - start reports\report.html