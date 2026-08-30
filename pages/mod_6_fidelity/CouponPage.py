from playwright.sync_api import Page, expect
from pages.base_page import BasePage
import re


class Coupon(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # --- NUOVO COUPON ---
        self.btn_nuovo_coupon = page.get_by_role("button", name="Nuovo Coupon")
        self.campo_tipo_coupon = page.get_by_label("Tipo coupon")
        self.input_valore = page.get_by_role("spinbutton", name="Valore")
        self.input_ordine_minimo = page.get_by_role("spinbutton", name="Ordine minimo")
        self.input_validita_giorni = page.get_by_role("spinbutton", name="Validità (giorni)")
        self.input_max_utilizzi = page.get_by_role("spinbutton", name="Max utilizzi")
        self.btn_genera = page.get_by_role("button", name="Genera", exact=True)

        # --- NUOVO COUPON CON PRODOTTO GRATIS ---
        
        self.campo_ricerca_prodotto_gratis = page.get_by_role("combobox", name="Prodotto gratis")

# ============================================================
# NAVIGAZIONE
# ============================================================

    def apri_coupon(self):
        self.apri_gruppo_menu("Fidelity")
        self.naviga_a("/fidelity/coupons")

# ============================================================
# NUOVO COUPON
# ============================================================

    def crea_nuovo_coupon(self):
        self.btn_nuovo_coupon.click()

    def seleziona_tipo_coupon(self, tipo: str):
        """Seleziona il tipo di coupon dal dropdown 'Tipo coupon'.
        Valori validi (visti nel form): 'Sconto Fisso', 'Sconto %', 'Prodotto Gratis'.
        Prima era hardcoded su 'Sconto Fisso' (seleziona_coupon), quindi ogni test
        selezionava sempre lo stesso tipo indipendentemente da cosa stava testando.
        """
        self.seleziona_option_per_testo_dropdown(self.campo_tipo_coupon, tipo)

    def compila_mod_nuovo_coupon(self, dati_coupon: dict):
        self.input_valore.fill(str(dati_coupon["valore"]))
        self.input_ordine_minimo.fill(str(dati_coupon["ordine minimo"]))
        self.input_validita_giorni.fill(str(dati_coupon["validita_giorni"]))
        self.input_max_utilizzi.fill(str(dati_coupon["max_utilizzi"]))

    # --- COUPON CON PRODOTTO GRATIS ---

    def cerca_e_seleziona_prodotto_gratis(self, nome_prodotto: str):
        """Cerca un prodotto per nome nel campo 'Prodotto gratis' e lo seleziona
        dal menu a tendina. Mancava il wait_for + click sull'opzione: prima il
        metodo si fermava dopo il fill, senza mai selezionare nulla dal menu
        (per questo il flusso 'Prodotto Gratis' non completava mai la selezione).
        """
        self.campo_ricerca_prodotto_gratis.click()
        self.campo_ricerca_prodotto_gratis.fill(nome_prodotto)

        opzione = self.page.get_by_text(nome_prodotto)
        opzione.wait_for(state="visible")
        opzione.click()

    def compila_mod_con_prodotti_gratis(self, dati_coupon: dict):
        self.input_ordine_minimo.fill(str(dati_coupon["ordine minimo"]))
        self.input_validita_giorni.fill(str(dati_coupon["validita_giorni"]))
        self.input_max_utilizzi.fill(str(dati_coupon["max_utilizzi"]))

    # --- SALVATAGGIO ---

    def genera_coupon(self):
        """Clicca 'Genera' e attende la risposta della chiamata di salvataggio,
        così il chiamante può controllare status_code/body invece di
        affidarsi solo alla scomparsa del loader."""
        return self.clicca_e_attendi_risposta(
            self.btn_genera,
            re.compile(r"/fidelity/coupons"),
        )