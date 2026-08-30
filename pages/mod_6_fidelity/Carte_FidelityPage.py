from playwright.sync_api import Page, expect
from pages.base_page import BasePage
import re

class CarteFidelity(BasePage):
    def __init__(self, page:Page):
        super().__init__(page)

        # --- NUOVA CARTA FEDELITY ---
        self.btn_nuova_carta = page.get_by_role("button", name="Nuova Carta")

        # --- COMPILA MODULO ---
        self.input_barcode = page.get_by_role("textbox", name="Barcode", exact=True)
        self.campo_ricerca_cliente = page.get_by_role("combobox", name="Cliente")
        self.input_punti = page.get_by_role("spinbutton", name="Punti")
        self.input_credito = page.get_by_role("spinbutton", name="Credito EUR")
        self.input_moltiplicatore = page.get_by_role("spinbutton", name="Moltiplicatore")
        self.campo_tier = (
            page.get_by_role("dialog")
            .locator(".v-select")
            .filter(has_text=re.compile(r"Tier"))
            .locator(".v-field__input")
        )

        self.campo_listino = (
            page.get_by_role("dialog")
            .locator(".v-select")
            .filter(has_text=re.compile(r"^Listino prezzi"))
            .locator(".v-field__input")
        )

        self.input_salva = page.get_by_role("button", name="Salva")

          # --- NAVIGAZIONE ---
    def apri_carte_fidelity(self):
        self.apri_gruppo_menu("Fidelity")
        self.naviga_a("/fidelity/cards")

        # --- CREA E COMPILA CARTA NUOVA ---
    
    def crea_nuova_carta(self):
        self.btn_nuova_carta.click()

    def cerca_e_seleziona_cliente(self, nome_cliente: str):
        self.campo_ricerca_cliente.click()
        self.campo_ricerca_cliente.fill(nome_cliente)

        opzione = self.page.get_by_role("option", name=nome_cliente)
        opzione.wait_for(state="visible")
        opzione.click()

    def compila_barcode(self,dati_mod):
        self.input_barcode.fill(dati_mod["barcode"])
        self.input_punti.fill(str(dati_mod["punti"]))
        self.input_credito.fill(str(dati_mod["credito"]))
        self.input_moltiplicatore.fill(str(dati_mod["moltiplicatore"]))

    def seleziona_tier_casuale(self):
        self.seleziona_option_casuale_dropdown_icona_in_modale(self.campo_tier)

    def seleziona_listino_casuale(self):
        self.seleziona_option_casuale_dropdown_icona_in_modale(self.campo_listino)
        self.input_salva.click()
