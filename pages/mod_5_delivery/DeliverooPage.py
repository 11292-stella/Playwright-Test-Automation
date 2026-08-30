from playwright.sync_api import Page, expect
from pages.base_page import BasePage
import re

class Deliveroo(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # --- SWITCH ----
        self.switch_deliveroo = page.get_by_role("checkbox", name="Abilita Deliveroo")
        self.switch_accetta = page.get_by_role("checkbox", name="Accetta automaticamente gli")

        # --- COMPILA MODALE ---
        self.input_id = page.get_by_role("textbox", name="ID punto vendita (site /")
        self.input_brand_id = page.get_by_role("textbox", name="Brand ID (rilevato dai punti")
        self.input_tempo_preparazione = page.get_by_role("spinbutton", name="Tempo preparazione (min)")
        self.input_ricarico_prezzo = page.get_by_role("spinbutton", name="Ricarico prezzo (%)")
        self.url_img = page.get_by_role("textbox", name="URL foto di copertina menù (")
        self.btn_salva_conf = page.get_by_role("button", name="Salva configurazione")

        # --- VERIFICA ID ---
        self.btn_aggiungi = page.get_by_role("button", name="Azione successiva ID punto")
        self.btn_verifica = page.get_by_role("button", name="Verifica")

        # --- TAB MENU ---
        self.tab_menu = page.get_by_role("tab", name="Menù")
        self.btn_nuova_categoria = page.get_by_role("button", name="Nuova Categoria")
        self.dropdown_importa_categoria = page.get_by_role("combobox", name="Importa da categoria prodotti")
        self.btn_aggiungi_img = page.get_by_role("button", name="Seleziona")
        self.seleziona_img = page.locator(".v-responsive__content")
        self.conferma_img = page.get_by_role("button", name="Conferma")
        self.btn_salva_finale = page.get_by_role("button", name="Salva")
        self.btn_assegna_negozi = page.get_by_role("button", name=re.compile(r"Assegna \d+ prodott"))
        

        # --- NAVIGAZIONE ---
    def apri_delivery(self):
        self.apri_gruppo_menu("Delivery")
        self.naviga_a("/delivery-integrations/deliveroo")

        # --- ABILITA E COMPILA INFO ---
    def abilita_deliveroo(self):
        self.switch_deliveroo.click()

    def compila_modulo_deliveroo(self,dati_deliveroo:dict):
        self.input_id.fill(dati_deliveroo["id"])
        self.input_tempo_preparazione.fill(dati_deliveroo["tempo_preparazione"])
        self.input_ricarico_prezzo.fill(dati_deliveroo["ricarico_prezzo"])
        self.url_img.fill(dati_deliveroo["url_foto"])
        

    def abilita_switch_accetta(self):
        self.switch_accetta.click()

    def salva_configurazione(self):
        self.btn_salva_conf.click()

         # --- TAB MENU ----
    def vai_a_menu(self):
        self.tab_menu.click()

        # --- COMPILA MODULO ---
    def crea_nuova_categoria(self):
        self.btn_nuova_categoria.click()

    def dropdown_importa(self,testo_opzione: str):
         self.seleziona_option_per_testo_dropdown_in_modale(self.dropdown_importa_categoria, testo_opzione)

    def aggiungi_img_categoria(self):
        self.btn_aggiungi_img.click()
        self.seleziona_img.click()
        self.conferma_img.click()
        self.btn_salva_finale.click()
        self.btn_assegna_negozi.click()

    def rimuovi_prodotti_ed_elimina_ultima_categoria(self):
        self.page.get_by_role("button", name="Gestisci Prodotti").last.click()
        self.page.get_by_role("button", name="Deseleziona Tutti").click()
        self.page.get_by_role("button", name=re.compile(r"Salva \(\d+ prodotti\)")).click()

        self.page.once("dialog", lambda dialog: dialog.accept())
        self.page.get_by_role("button", name="Elimina").last.click()

        # --- VERIFICA ID ---

    def compila_solo_id(self,dati_id):
        self.input_id.fill(dati_id["id"])
        self.btn_aggiungi.click()
        self.btn_verifica.click()

       
