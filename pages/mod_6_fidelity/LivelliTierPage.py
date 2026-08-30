from playwright.sync_api import Page, expect
from pages.base_page import BasePage
import re

class LivelliTier(BasePage):
    def __init__(self, page:Page):
        super().__init__(page)

        # --- NUOVO TIER ---
        self.btn_nuovo_tier = page.get_by_role("button", name="Nuovo Tier")
        self.input_nome = page.get_by_role("textbox", name="Nome")
        self.input_livello = page.get_by_role("spinbutton", name="Livello")
        self.input_soglia_punti = page.get_by_role("spinbutton", name="Soglia Punti")
        self.input_moltiplicatore_punti = page.get_by_role("spinbutton", name="Moltiplicatore Punti")
        self.input_sconto = page.get_by_role("spinbutton", name="Sconto %")
        self.input_mesi  = page.get_by_role("spinbutton", name="Periodo Mantenimento (mesi)")
        self.input_colore = page.get_by_role("textbox", name="Colore")
        self.input_icona = page.get_by_role("textbox", name="Icona")
        self.campo_listino = (
                    page.get_by_role("dialog")
                    .locator(".v-select")
                    .filter(has_text=re.compile(r"^Listino prezzi"))
                    .locator(".v-field__input")
                )
        self.input_salva = page.get_by_role("button", name="Salva")

# ============================================================
# NAVIGAZIONE
# ============================================================

    def apri_livelli_tier(self):
        self.apri_gruppo_menu("Fidelity")
        self.naviga_a("/fidelity/tiers")

# ============================================================
# NUOVO TIER
# ============================================================
    def apri_nuovo_tier(self):
        self.btn_nuovo_tier.click()

    def compila_tier(self, dati_tier: dict):
        self.input_nome.fill(dati_tier["nome"])
        self.input_livello.fill(str(dati_tier["livello"]))
        self.input_soglia_punti.fill(str(dati_tier["soglia_punti"]))
        self.input_moltiplicatore_punti.fill(str(dati_tier["moltiplicatore"]))
        self.input_sconto.fill(str(dati_tier["sconto"]))
        self.input_mesi.fill(str(dati_tier["mesi"]))
        self.input_colore.fill(dati_tier["colore"])
        self.input_icona.fill(dati_tier["icona"])

    def seleziona_listino_casuale(self):
        self.seleziona_option_casuale_dropdown_icona_in_modale(self.campo_listino)
        self.input_salva.click()
        