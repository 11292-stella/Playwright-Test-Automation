from playwright.sync_api import Page
from pages.base_page import BasePage
import re

class WebAppTavoloCatalogo(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # --- APRI TAB ---
        self.apri_tab_app_tavolo_catalogo = page.get_by_role("tab", name="Webapp Tavolo - Catalogo")

        # --- NUOVA CATEGORIA ---
        self.btn_nuova_categoria = page.get_by_role("button", name="Nuova Categoria")
        self.combobox_importa_categoria = page.get_by_role("combobox", name="Importa da categoria prodotti")
        self.btn_img = page.get_by_role("button", name="Seleziona")
        self.btn_img_selezionata = page.locator(".v-responsive__content")
        self.btn_conferma_img = page.get_by_role("button", name="Conferma")
        self.input_descrizione = page.get_by_role("textbox", name="Descrizione")
        self.input_ordine = page.get_by_role("spinbutton", name="Ordine Visualizzazione")
        self.btn_salva_finale = page.get_by_role("button", name="Salva")

         # --- BOTTONE ASSEGNA (numero prodotti dinamico) ---
        self.btn_assegna_prodotti = page.get_by_role(
            "button", name=re.compile(r"Assegna \d+ prodott[oi]")
        )



        # --- NAVIGAZIONE ---
    def apri_app_tavolo_catalogo(self):
        self.apri_gruppo_menu("Gestione Locale")
        self.naviga_a("/restaurant-config")
        self.apri_tab_app_tavolo_catalogo.click()

        # --- NUOVA CATEGORIA ---
    def nuova_categoria_mod(self):
        self.btn_nuova_categoria.click()

    def seleziona_categoria_importa(self, nome_categoria: str):
        self.seleziona_option_per_testo_dropdown(self.combobox_importa_categoria, nome_categoria)

    def seleziona_img(self):
        self.btn_img.click()
        self.btn_img_selezionata.click()
        self.btn_conferma_img.click()

    def compila_categoria(self,dati_categoria:dict):
        self.input_descrizione.fill(dati_categoria["descrizione"])
        self.input_ordine.fill(str(dati_categoria["ordine"]))
        self.btn_salva_finale.click()

    def assegna_prodotti(self):
        self.btn_assegna_prodotti.click()