import random

from playwright.sync_api import expect
from pages.mod_6_fidelity.ImpostazioniPage import Impostazioni
from utils.test_data import ChainTestData


class TestImpostazioni:

    # --- TAB FIDELITY ---
    # Smoke: il toggle "Pagamento con Punti" parte spento per default,
    # verifichiamo solo che il click lo attivi (comportamento UI puro,
    # nessun salvataggio coinvolto).
    def test_impostazioni_fidelity(self, authenticated_page):
        imp = Impostazioni(authenticated_page)
        imp.apri_impostazioni()

        imp.compila_regola_accumulo_punti(punti=1, ogni_euro=1)

        assert not imp.switch_pagamento_con_punti.is_checked()
        imp.toggla_pagamento_con_punti()
        assert imp.switch_pagamento_con_punti.is_checked()

    # --- TAB PREPAGATE ---
    # Smoke: i campi accettano i valori e li mantengono — non testiamo
    # il salvataggio, solo che il form si compili senza errori bloccanti.
    def test_impostazioni_prepagate(self, authenticated_page):
        imp = Impostazioni(authenticated_page)
        imp.apri_impostazioni()
        imp.vai_a_prepagate()

        dati_prepagata = ChainTestData.genera_dati_prepagata()
        imp.compila_limiti_prepagata(dati_prepagata)

        expect(imp.input_saldo_massimo_carta).to_have_value(str(dati_prepagata["saldo_massimo_carta"]))

    # --- TAB WALLET ---
    # Smoke: apre il tab, compila il nome programma, clicca Salva.
    # Non asseriamo l'esito del salvataggio (fuori scope per un test
    # "tanto per" su una sezione di impostazioni marginale).
    def test_impostazioni_wallet(self, authenticated_page):
        imp = Impostazioni(authenticated_page)
        imp.apri_impostazioni()
        imp.vai_a_wallet()

        imp.compila_aspetto_pass(f"Programma Test {random.randint(1000, 9999)}")
        imp.salva_aspetto()

        
# per avviare il test: - pytest tests/6_fidelity/test_impostazioni.py --headed
# per avviare il test di tutta la cartella gestione_catene: - pytest tests/6_fidelity
# per aprire il report finale: - start reports\report.html