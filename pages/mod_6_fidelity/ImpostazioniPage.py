from playwright.sync_api import Page, expect
from pages.base_page import BasePage
import re


class Impostazioni(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # --- TAB ---
        self.tab_prepagate = page.get_by_role("tab", name="Prepagate")
        self.tab_wallet = page.get_by_role("tab", name="Wallet")

        # --- TAB FIDELITY: ACCUMULO PUNTI ---
        self.switch_abilita_accumulo_punti = page.get_by_role(
            "checkbox", name="Abilita accumulo punti sugli acquisti"
        )
        self.input_punti_accreditati = page.get_by_role("spinbutton", name="Punti accreditati")
        self.input_ogni_quanti_euro = page.get_by_role("spinbutton", name="Ogni quanti euro")

        # --- TAB FIDELITY: ACQUISTI CON PREPAGATA ---
        self.switch_accumula_con_prepagata = page.get_by_role(
            "checkbox", name="Accumula punti anche pagando con credito prepagato"
        )

        # --- TAB FIDELITY: PAGAMENTO CON PUNTI ---
        self.switch_pagamento_con_punti = page.get_by_role(
            "checkbox", name="Consenti di usare i punti fidelity per pagare"
        )

        # --- TAB FIDELITY: STAMPA SCONTRINO ---
        self.switch_stampa_riepilogo = page.get_by_role(
            "checkbox", name="Stampa riepilogo fidelity in coda allo scontrino"
        )

        # --- TAB PREPAGATE ---
        self.input_importo_minimo_ricarica = page.get_by_role("spinbutton", name="Importo minimo ricarica (EUR)")
        self.input_importo_massimo_ricarica = page.get_by_role("spinbutton", name="Importo massimo ricarica (EUR)")
        self.input_saldo_massimo_carta = page.get_by_role("spinbutton", name="Saldo massimo carta (EUR)")
        self.input_scadenza_credito = page.get_by_role("spinbutton", name="Scadenza credito (mesi)")

        # --- TAB WALLET ---
        self.input_nome_programma = page.get_by_role("textbox", name="Nome programma (es. nome ristorante)")
        self.btn_salva_aspetto = page.get_by_role("button", name="Salva aspetto")

# ============================================================
# NAVIGAZIONE
# ============================================================

    def apri_impostazioni(self):
        self.apri_gruppo_menu("Fidelity")
        self.naviga_a("/fidelity/impostazioni")

    def vai_a_prepagate(self):
        self.tab_prepagate.click()

    def vai_a_wallet(self):
        self.tab_wallet.click()

# ============================================================
# TAB FIDELITY
# ============================================================

    def toggla_pagamento_con_punti(self):
        """Il toggle parte disattivato di default (vedi screenshot):
        cliccandolo lo attiva, verificabile con .is_checked()."""
        self.switch_pagamento_con_punti.click()

    def compila_regola_accumulo_punti(self, punti: int, ogni_euro: int):
        self.input_punti_accreditati.fill(str(punti))
        self.input_ogni_quanti_euro.fill(str(ogni_euro))

# ============================================================
# TAB PREPAGATE
# ============================================================

    def compila_limiti_prepagata(self, dati_prepagata: dict):
        self.input_importo_minimo_ricarica.fill(str(dati_prepagata["importo_minimo_ricarica"]))
        self.input_importo_massimo_ricarica.fill(str(dati_prepagata["importo_massimo_ricarica"]))
        self.input_saldo_massimo_carta.fill(str(dati_prepagata["saldo_massimo_carta"]))
        self.input_scadenza_credito.fill(str(dati_prepagata["scadenza_credito_mesi"]))

# ============================================================
# TAB WALLET
# ============================================================

    def compila_aspetto_pass(self, nome_programma: str):
        self.input_nome_programma.fill(nome_programma)

    def salva_aspetto(self):
        self.btn_salva_aspetto.click()