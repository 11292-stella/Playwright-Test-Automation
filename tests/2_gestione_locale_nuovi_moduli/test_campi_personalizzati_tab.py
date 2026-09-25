import pytest
from pages.mod_2_gestione_locale_nuovi_moduli.Campi_personalizzatiPage import CampiPersonalizzati
from utils.test_data import ChainTestData

TABS_DA_TESTARE = [
    "Nuclei familiari",
    "Unità tracciate (lotti e seriali)",
    "Prodotti",
    "Fornitori",
    "Prenotazioni",
    "Appuntamenti",
    "Soci palestra",
    "Abbonamenti",
    "Lead palestra",
]


class TestCampiPersonalizzatiSmoke:

    @pytest.mark.parametrize("nome_tab", TABS_DA_TESTARE)
    def test_creazione_minima_per_tab(self, authenticated_page, nome_tab):
        campi = CampiPersonalizzati(authenticated_page)
        campi.apri_campi_personalizzati()
        campi.vai_a_tab(nome_tab)

        dati = ChainTestData.genera_dati_campi_personalizzati_nuovo_campo_univoco()
        campi.crea_campo_minimo(dati["etichetta"], dati["descrizione"])



# per avviare il test: - pytest tests/2_gestione_locale_nuovi_moduli/test_campi_personalizzati_tab.py --headed
# per avviare il test di tutta la cartella gestione locale nuovi moduli: - pytest tests/2_gestione_locale_nuovi_moduli
# per aprire il report finale: - start reports\report.html