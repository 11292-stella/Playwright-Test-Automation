from playwright.sync_api import Page, expect
from pages.base_page import BasePage
import re


class Premi(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # --- SWITCH ---
        self.switch_mostra_in_cassa = (
            page.locator(".v-card")
            .filter(has_text="Mostra in cassa solo i premi riscattabili dal cliente")
            .locator("input[type='checkbox']")
        )
        self.switch_avvisa_in_cassa = (
            page.locator(".v-card")
            .filter(has_text="Avvisa in cassa quando il cliente ha raggiunto un premio")
            .locator("input[type='checkbox']")
        )

        # --- NUOVO PREMIO: CAMPI COMUNI A TUTTI I TIPI ---
        self.btn_nuovo_premio = page.get_by_role("button", name="Nuovo Premio")
        self.input_nome = page.get_by_role("textbox", name="Nome")
        self.input_descrizione = page.get_by_role("textbox", name="Descrizione")
        self.input_punti_richiesti = page.get_by_role("spinbutton", name="Punti Richiesti")
        self.input_stock = page.get_by_role("spinbutton", name="Stock (-1 = illimitato)")
        self.tipo_premio_dropdown = page.get_by_label("Tipo Premio")

        self.campo_tier = (
            page.get_by_role("dialog")
            .locator(".v-select")
            .filter(has_text=re.compile(r"Tier"))
            .locator(".v-field__input")
        )
        self.btn_salva = page.get_by_role("button", name="Salva")

        # --- TIPO PREMIO: SCONTO (default) ---
        # Campo "Tipo Sconto" (es. Sconto % / Sconto Fisso / Prodotto Gratis)
        # visibile SOLO quando "Tipo Premio" è sul valore di default "Sconto".
        # NOTA: non confondere con campo_tipo_coupon qui sotto — sono due
        # campi diversi, con label diversa, che compaiono in due stati
        # differenti della stessa modale "Nuovo Premio".
        self.campo_tipo_sconto = page.get_by_label("Tipo Sconto")
        self.input_valore_sconto = page.get_by_role("spinbutton", name="Valore Sconto")

        # --- TIPO PREMIO: PRODOTTO GRATIS ---
        self.campo_ricerca_prodotto_gratis = page.locator(
            ".v-field.v-field--appended.v-field--center-affix.v-field--prepended.v-field--variant-filled"
        ).locator("input")

        # --- TIPO PREMIO: CREDITO ---
        self.input_credito = page.get_by_role("spinbutton", name="Credito EUR")

        # --- TIPO PREMIO: COUPON ---
        # Campo "Tipo coupon" (es. Sconto % / Sconto Fisso / Prodotto Gratis)
        # visibile SOLO quando "Tipo Premio" = "Coupon". Stessa lista di
        # opzioni del campo_tipo_sconto, ma label diversa ("Tipo coupon"
        # minuscolo) perché è un campo distinto nel form.
        self.campo_tipo_coupon = page.get_by_label("Tipo coupon")
        self.input_valore = page.get_by_role("spinbutton", name="Valore")
        self.input_max_utilizzi = page.get_by_role("spinbutton", name="Max utilizzi")
        self.input_ordine_minimo = page.get_by_role("spinbutton", name="Ordine minimo")
        self.input_validita_giorni = page.get_by_role("spinbutton", name="Validità (giorni)")

    # ============================================================
    # NAVIGAZIONE
    # ============================================================

    def apri_premi(self):
        self.apri_gruppo_menu("Fidelity")
        self.naviga_a("/fidelity/rewards")

    # ============================================================
    # SWITCH
    # ============================================================

    def abilita_switch(self):
        self.switch_mostra_in_cassa.click()
        self.switch_avvisa_in_cassa.click()

    # ============================================================
    # NUOVO PREMIO: APERTURA MODALE / CAMPI COMUNI
    # ============================================================

    def crea_nuovo_premio(self):
        self.btn_nuovo_premio.click()

    def compila_premio(self, dati_premio: dict):
        """Compila i campi comuni al form di default (Tipo Premio = Sconto)."""
        self.input_nome.fill(dati_premio["nome"])
        self.input_descrizione.fill(dati_premio["descrizione"])
        self.input_punti_richiesti.fill(str(dati_premio["punti_richiesti"]))
        self.input_valore_sconto.fill(str(dati_premio["valore_sconto"]))
        self.input_stock.fill(str(dati_premio["stock"]))

    def seleziona_tier_casuale(self):
        self.seleziona_option_casuale_dropdown_icona_in_modale(self.campo_tier)
        self.btn_salva.click()

    # ============================================================
    # TIPO PREMIO: SCONTO
    # ============================================================

    def seleziona_tipo_sconto_casuale(self):
        """Seleziona un'opzione casuale nel campo 'Tipo Sconto'
        (Sconto % / Sconto Fisso / Prodotto Gratis), visibile quando
        Tipo Premio = Sconto (default)."""
        self.seleziona_option_casuale_dropdown_icona_in_modale(self.campo_tipo_sconto)

    # ============================================================
    # TIPO PREMIO: PRODOTTO GRATIS
    # ============================================================

    def seleziona_tipo_prodotto_gratis(self):
        self.seleziona_option_per_testo_dropdown(self.tipo_premio_dropdown, "Prodotto Gratis")

    def cerca_e_seleziona_prodotto_gratis(self, nome_prodotto: str):
        self.campo_ricerca_prodotto_gratis.click()
        self.campo_ricerca_prodotto_gratis.fill(nome_prodotto)

        opzione = self.page.get_by_text(nome_prodotto)
        opzione.wait_for(state="visible")
        opzione.click()

    # ============================================================
    # TIPO PREMIO: CREDITO
    # ============================================================

    def seleziona_credito(self):
        self.seleziona_option_per_testo_dropdown(self.tipo_premio_dropdown, "Credito")

    def compila_mod_con_credito(self, dati_premio: dict):
        self.input_nome.fill(dati_premio["nome"])
        self.input_descrizione.fill(dati_premio["descrizione"])
        self.input_punti_richiesti.fill(str(dati_premio["punti_richiesti"]))
        self.input_credito.fill(str(dati_premio["valore_sconto"]))
        self.input_stock.fill(str(dati_premio["stock"]))

    # ============================================================
    # TIPO PREMIO: COUPON
    # ============================================================

    def seleziona_coupon(self):
        self.seleziona_option_per_testo_dropdown(self.tipo_premio_dropdown, "Coupon")

    def compila_mod_coupon(self, dati_premio: dict):
        self.input_nome.fill(dati_premio["nome"])
        self.input_descrizione.fill(dati_premio["descrizione"])
        self.input_punti_richiesti.fill(str(dati_premio["punti_richiesti"]))
        self.input_max_utilizzi.fill(str(dati_premio["max_utilizzi"]))
        self.input_valore.fill(str(dati_premio["valore"]))
        self.input_ordine_minimo.fill(str(dati_premio["ordine minimo"]))
        self.input_validita_giorni.fill(str(dati_premio["validita_giorni"]))
        self.input_stock.fill(str(dati_premio["stock"]))

    def seleziona_tipo_coupon_casuale(self):
        
        self.seleziona_option_casuale_dropdown_icona_in_modale(self.campo_tipo_coupon)



