from playwright.sync_api import Page
from pages.base_page import BasePage
import random

class CatalogoApp(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # --- SELEZIONA TAB ---
        self.apri_tab_catalogo_app = page.get_by_role("tab", name="Catalogo App")

        # --- DROPDOWN CATEGORIA ---
        self.dropdown_categoria = page.locator(".v-select").filter(has_text="Categorie").locator(".v-field__input")

        # --- MENU APP TAB ---
        self.btn_tab_menu = page.get_by_role("tab", name="Menù App")
        self.btn_nuovo_menu = page.get_by_role("button", name="Nuovo Menù")
        self.input_nome_menu_it = page.get_by_role("textbox", name="Nome Menù (IT)")
        self.input_nome_menu_ing = page.get_by_role("textbox", name="Nome Menù (EN)")
        self.input_prezzo_fisso = page.get_by_role("spinbutton", name="Prezzo Fisso")
        self.input_descrizione = page.get_by_role("textbox", name="Descrizione (IT)")
        self.input_img = page.get_by_role("textbox", name="URL Immagine")

        # --- GIORNI DISPONIBILITÀ ---
        self.giorno_lun = page.get_by_text("Lun", exact=True)
        self.giorno_mar = page.get_by_text("Mar", exact=True)
        self.giorno_mer = page.get_by_text("Mer", exact=True)
        self.giorno_gio = page.get_by_text("Gio", exact=True)
        self.giorno_ven = page.get_by_text("Ven", exact=True)
        self.giorno_sab = page.get_by_text("Sab", exact=True)
        self.giorno_dom = page.get_by_text("Dom", exact=True)
        self.giorni_disponibili = [
            self.giorno_lun, self.giorno_mar, self.giorno_mer,
            self.giorno_gio, self.giorno_ven, self.giorno_sab, self.giorno_dom,
        ]

        # --- DATE DISPONIBILITÀ ---
        self.input_data_inizio = page.get_by_role("textbox", name="Data inizio")
        self.input_data_fine = page.get_by_role("textbox", name="Data fine")
        self.input_salva = page.get_by_role("button", name="Salva")


        
           # --- NAVIGAZIONE ---
    def apri_app_catalogo(self):
        self.apri_gruppo_menu("Gestione Locale")
        self.naviga_a("/restaurant-config")
        self.apri_tab_catalogo_app.click()
        
        # --- SELEZIONA CATEGORIA ---
    def seleziona_categoria(self, nome_categoria: str):
     self.seleziona_option_per_testo_dropdown_icona(self.dropdown_categoria, nome_categoria)

        # --- TAB MENU ---
    def apri_tab_menu(self):
       self.btn_tab_menu.click()
       self.btn_nuovo_menu.click()

    def compila_nuovo_menu(self, dati_menu: dict):
        self.input_nome_menu_it.fill(dati_menu["nome_menu_it"])
        self.input_nome_menu_ing.fill(dati_menu["nome_menu_ing"])
        self.input_prezzo_fisso.fill(str(dati_menu["prezzo_fisso"]))
        self.input_descrizione.fill(dati_menu["descrizione_it"])
        self.input_img.fill(dati_menu["url_img"])

    def seleziona_giorno_random(self):
        random.choice(self.giorni_disponibili).click()

    def compila_date_disponibilita(self, data_inizio: str, data_fine: str):
     self.compila_data(self.input_data_inizio, data_inizio)
     self.compila_data(self.input_data_fine, data_fine)
     self.input_salva.click()
