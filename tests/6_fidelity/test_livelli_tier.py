from pages.mod_6_fidelity.LivelliTierPage import LivelliTier
from utils.test_data import ChainTestData

class TestTier:
    def test_tier(self,authenticated_page):
        tier = LivelliTier(authenticated_page)
        tier.apri_livelli_tier()

        tier.apri_nuovo_tier()
        dati_tier = ChainTestData.genera_dati_tier()
        tier.compila_tier(dati_tier)
        tier.seleziona_listino_casuale()



# per avviare il test: - pytest tests/6_fidelity/test_livelli_tier.py --headed
# per avviare il test di tutta la cartella gestione_catene: - pytest tests/6_fidelity
# per aprire il report finale: - start reports\report.html