from playwright.sync_api import Page
from pages.base_page import BasePage
import random

class AppAsportoPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # --- SELEZIONA TAB ---
        self.apri_tab_asporto = page.get_by_role("tab", name="App Asporto", exact=True)
        self.apri_tab_testi = page.get_by_role("tab", name="Testi")
        self.btn_di_scorrimento = page.locator(".mdi-chevron-right").first
        self.apri_tab_loghi_e_immagini = page.get_by_role("tab", name="Loghi e Immagini")
        self.btn_salva = page.get_by_role("button", name="Salva")


        # --- SELEZIONA TEMA ---
        self.selezione_tema_classico = page.get_by_text("Classico")
        self.seleziona_tema_elegante = page.get_by_text("Elegante")
        self.seleziona_tema_moderno = page.get_by_text("Moderno")
        self.seleziona_tema_dark = page.get_by_text("Dark")

        self.temi_disponibili = [
            self.selezione_tema_classico,
            self.seleziona_tema_elegante,
            self.seleziona_tema_moderno,
            self.seleziona_tema_dark,
        ]
        

        # --- COMPILA MOD Branding App Asporto ---
        self.input_facebook = page.get_by_role("textbox", name="Facebook")
        self.input_instagram = page.get_by_role("textbox", name="Instagram")
        self.input_tik_tok = page.get_by_role("textbox", name="TikTok")
        self.input_google_maps = page.get_by_role("textbox", name="Google Maps")

        # --- COMPILA TAB TESTO ---
        self.input_slogan = page.get_by_role("textbox", name="Slogan / Tagline")
        self.input_mes_benvenuto = page.get_by_role("textbox", name="Messaggio di Benvenuto")
        self.input_mess_ora_chiusura = page.get_by_role("textbox", name="Messaggio Orario Chiuso")
        self.input_testo_footer = page.get_by_role("textbox", name="Testo Footer")
        self.input_info_consegna = page.get_by_role("textbox", name="Info Consegna")
        self.input_note_legali = page.get_by_role("textbox", name="Note Legali / Privacy")

        # --- COMPILA TAB LOGHI E IMMAGINI ---
        self.input_logo_principale = page.get_by_role("textbox", name="Logo Principale")
        self.input_logo_secondario = page.get_by_role("textbox", name="Logo Secondario")
        self.input_favicon = page.get_by_role("textbox", name="Favicon")
        self.input_immagine_hero = page.get_by_role("textbox", name="Immagine Hero")
        self.input_pattern_sfondo = page.get_by_role("textbox", name="Pattern Sfondo")
        

        

        # --- NAVIGAZIONE ---
    def apri_app_asporto_servizi(self):
        self.apri_gruppo_menu("Gestione Locale")
        self.naviga_a("/restaurant-config")
        self.apri_tab_asporto.click()

        # --- SELEZIONA TEMA RANDOM ---
    def seleziona_tema_random(self):
        random.choice(self.temi_disponibili).click()

        # --- COMPILA MODULO BRANDING APP ASPORTO ---
    def compila_social_mod(self, dati_social:dict):
        self.input_facebook.fill(dati_social["facebook"])
        self.input_instagram.fill(dati_social["instagram"])
        self.input_tik_tok.fill(dati_social["tik_tok"])
        self.input_google_maps.fill(dati_social["google_maps"])

        # --- TAB TESTI COMPILAZIONE ---
    def seleziona_tab_testi(self):
        self.apri_tab_testi.click()

        # --- COMPILA TAB TESTO ---
    def compila_tab_testi(self, dati_testi: dict):
        self.input_slogan.fill(dati_testi["slogan"])
        self.input_mes_benvenuto.fill(dati_testi["mess_benvenuto"])
        self.input_mess_ora_chiusura.fill(dati_testi["mess_orario_chiusura"])
        self.input_testo_footer.fill(dati_testi["testo_footer"])
        self.input_info_consegna.fill(dati_testi["info_consegna"])
        self.input_note_legali.fill(dati_testi["note_legali"])


        # --- COMPILA TAB LOGHI E IMMAGINI ---
    def click_doppio_btn(self):
        self.btn_di_scorrimento.click()
        self.btn_di_scorrimento.click()
        self.apri_tab_loghi_e_immagini.click()

    def compila_tab_loghi_e_immagini(self, dati_loghi: dict):
        self.input_logo_principale.fill(dati_loghi["logo_principale"])
        self.input_logo_secondario.fill(dati_loghi["logo_secondario"])
        self.input_favicon.fill(dati_loghi["favicon"])
        self.input_immagine_hero.fill(dati_loghi["immagine_hero"])
        self.input_pattern_sfondo.fill(dati_loghi["pattern_sfondo"])
        self.btn_salva.click()