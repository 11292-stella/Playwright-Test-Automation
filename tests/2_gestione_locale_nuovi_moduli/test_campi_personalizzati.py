import pytest
from pages.mod_2_gestione_locale_nuovi_moduli.Campi_personalizzatiPage import CampiPersonalizzati
from utils.test_data import ChainTestData


class TestCampiPersonalizzati:

    def test_campo_semplice_senza_extra(self, authenticated_page):
        """Tipo senza campi extra (es. Testo) - happy path base."""
        campi = CampiPersonalizzati(authenticated_page)
        campi.apri_campi_personalizzati()
        campi.crea_nuovo_campo()

        dati_campo = ChainTestData.genera_dati_campi_personalizzati_nuovo_campo()
        campi.compila_campo(dati_campo)
        campi.seleziona_tipo_dato("testo")

    def test_campo_numero_decimale(self, authenticated_page):
        """Tipo con min/max numerico."""
        campi = CampiPersonalizzati(authenticated_page)
        campi.apri_campi_personalizzati()
        campi.crea_nuovo_campo()

        dati_campo = ChainTestData.genera_dati_campi_personalizzati_nuovo_campo()
        campi.compila_campo(dati_campo)

        dati_stato = ChainTestData.genera_dati_campi_aggiuntivi_tipo_dato()
        campi.seleziona_tipo_dato("numero_decimale", dati_stato)

    def test_campo_selezione_singola(self, authenticated_page):
        """Tipo con N opzioni da aggiungere."""
        campi = CampiPersonalizzati(authenticated_page)
        campi.apri_campi_personalizzati()
        campi.crea_nuovo_campo()

        dati_campo = ChainTestData.genera_dati_campi_personalizzati_nuovo_campo()
        campi.compila_campo(dati_campo)

        dati_stato = ChainTestData.genera_dati_campi_aggiuntivi_tipo_dato(n_opzioni=3)
        campi.seleziona_tipo_dato("selezione_singola", dati_stato)

    def test_campo_selezione_multipla(self, authenticated_page):
        """Tipo con opzioni + selezioni minime/massime."""
        campi = CampiPersonalizzati(authenticated_page)
        campi.apri_campi_personalizzati()
        campi.crea_nuovo_campo()

        dati_campo = ChainTestData.genera_dati_campi_personalizzati_nuovo_campo()
        campi.compila_campo(dati_campo)

        dati_stato = ChainTestData.genera_dati_campi_aggiuntivi_tipo_dato(n_opzioni=3)
        campi.seleziona_tipo_dato("selezione_multipla", dati_stato)

    def test_campo_diario(self, authenticated_page):
        """Tipo con opzioni + caratteri/voci conservate."""
        campi = CampiPersonalizzati(authenticated_page)
        campi.apri_campi_personalizzati()
        campi.crea_nuovo_campo()

        dati_campo = ChainTestData.genera_dati_campi_personalizzati_nuovo_campo()
        campi.compila_campo(dati_campo)

        dati_stato = ChainTestData.genera_dati_campi_aggiuntivi_tipo_dato(n_opzioni=3)
        campi.seleziona_tipo_dato("diario", dati_stato)

    def test_salvataggio_reale_campo(self, authenticated_page):
        """Unico test che salva davvero: usa un'etichetta univoca per evitare conflitti."""
        campi = CampiPersonalizzati(authenticated_page)
        campi.apri_campi_personalizzati()
        campi.crea_nuovo_campo()

        dati_campo = ChainTestData.genera_dati_campi_personalizzati_nuovo_campo_univoco()
        campi.compila_campo(dati_campo)
        campi.seleziona_tipo_dato("testo")
        campi.seleziona_opzioni_visibilita()
        campi.salva_campo()


# per avviare tutti: pytest tests/2_gestione_locale_nuovi_moduli/test_campi_personalizzati.py --headed