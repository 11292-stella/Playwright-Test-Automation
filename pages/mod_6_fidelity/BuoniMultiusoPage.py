from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class BuoniMultiuso(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # --- EMETTI BUONO ---
        self.btn_emetti_buono = page.get_by_role("button", name="Emetti Buono")
        self.input_valore = page.get_by_role("spinbutton", name="Valore (EUR)")
        self.input_validita_giorni = page.get_by_role("spinbutton", name="Validita (giorni)")
        self.input_id_cliente = page.get_by_role("textbox", name="ID Cliente (opzionale)")

       
        self.btn_emetti = page.get_by_role("button", name="Emetti", exact=True)

# ============================================================
# NAVIGAZIONE
# ============================================================

    def apri_buoni_multiuso(self):
        self.apri_gruppo_menu("Fidelity")
        self.naviga_a("/fidelity/gift-cards")

# ============================================================
# EMETTI BUONO
# ============================================================

    def apri_modale_emetti_buono(self):
        self.btn_emetti_buono.click()

    def compila_buono(self, dati_buono: dict):
        """Compila il form 'Emetti Buono'. 'id_cliente' è opzionale nel form:
        se non presente nel dizionario, il campo viene lasciato vuoto."""
        self.input_valore.fill(str(dati_buono["valore"]))
        self.input_validita_giorni.fill(str(dati_buono["validita_giorni"]))

        id_cliente = dati_buono.get("id_cliente")
        if id_cliente:
            self.input_id_cliente.fill(str(id_cliente))

    def emetti_buono(self):
        """Clicca 'Emetti'.

        BUG NOTO (backend): la collection gift_cards ha un indice UNIQUE
        non-sparse su 'idempotencyKey', salvato sempre come null — solo la
        prima emissione in assoluto va a buon fine, tutte le successive
        falliscono (MongoServerError E11000, dup key: idempotencyKey: null).
        Riprodotto sia da UI manuale che da test.
        """
        self.btn_emetti.click()