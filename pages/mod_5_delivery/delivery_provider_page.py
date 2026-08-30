from playwright.sync_api import Page
from pages.base_page import BasePage
import re


class DeliveryProviderPage(BasePage):
    """Classe base per i provider Delivery (Deliveroo, Just Eat, Uber Eats,
    Glovo, Deliverect). Contiene tutto ciò che è identico tra i provider.

    Ogni subclass definisce nel proprio __init__:
    - self.path             (path di navigazione del provider)
    - self.switch_provider  (checkbox "Abilita X", nome cambia per provider)
    - i campi ID specifici  (numero e nomi diversi tra provider)
    """

    def __init__(self, page: Page):
        super().__init__(page)

        # --- CAMPI COMUNI A TUTTI I PROVIDER ---
        self.switch_accetta = page.get_by_role("checkbox", name="Accetta automaticamente gli")
        self.input_tempo_preparazione = page.get_by_role("spinbutton", name="Tempo preparazione (min)")
        self.input_ricarico_prezzo = page.get_by_role("spinbutton", name="Ricarico prezzo (%)")
        self.url_img = page.get_by_role("textbox", name="URL foto di copertina menù")
        self.btn_salva_conf = page.get_by_role("button", name="Salva configurazione")

        # --- TAB MENU ---
        self.tab_menu = page.get_by_role("tab", name="Menù")
        self.btn_nuova_categoria = page.get_by_role("button", name="Nuova Categoria")
        self.dropdown_importa_categoria = page.get_by_role("combobox", name="Importa da categoria prodotti")
        self.btn_aggiungi_img = page.get_by_role("button", name="Seleziona")
        self.seleziona_img = page.locator(".v-responsive__content")
        self.conferma_img = page.get_by_role("button", name="Conferma")
        self.btn_salva_finale = page.get_by_role("button", name="Salva")
        self.btn_assegna_prodotti = page.get_by_role("button", name=re.compile(r"Assegna \d+ prodott"))
        self.btn_gestisci_prodotti = page.get_by_role("button", name="Gestisci Prodotti")
        self.btn_deseleziona_tutti = page.get_by_role("button", name="Deseleziona Tutti")
        self.btn_salva_prodotti = page.get_by_role("button", name=re.compile(r"Salva \(\d+ prodotti\)"))
        self.btn_elimina_categoria = page.get_by_role("button", name="Elimina")

        # --- da definire nella subclass ---
        self.switch_provider = None
        self.path = None

    # --- NAVIGAZIONE ---
    def apri_provider(self):
        self.apri_gruppo_menu("Delivery")
        self.naviga_a(self.path)

    def abilita_provider(self):
        self.switch_provider.click()

    def abilita_switch_accetta(self):
        self.switch_accetta.click()

    # --- CAMPI COMUNI ---
    def compila_campi_comuni(self, dati: dict):
        self.input_tempo_preparazione.fill(dati["tempo_preparazione"])
        self.input_ricarico_prezzo.fill(dati["ricarico_prezzo"])
        self.url_img.fill(dati["url_foto"])

    def salva_configurazione(self):
        self.btn_salva_conf.click()

    # --- TAB MENU ---
    def vai_a_menu(self):
        self.tab_menu.click()

    def crea_nuova_categoria(self):
        self.btn_nuova_categoria.click()

    def dropdown_importa(self, testo_opzione: str):
        self.seleziona_option_per_testo_dropdown_in_modale(self.dropdown_importa_categoria, testo_opzione)

    def aggiungi_img_categoria(self):
        self.btn_aggiungi_img.click()
        self.seleziona_img.click()
        self.conferma_img.click()
        self.btn_salva_finale.click()
        self.btn_assegna_prodotti.click()

    def leggi_numero_categorie(self) -> int:
        testo = self.page.get_by_text(re.compile(r"\d+ categorie?")).inner_text()
        return int(re.search(r"\d+", testo).group())

    # --- CLEANUP ---
    def rimuovi_prodotti_ed_elimina_ultima_categoria(self):
        self.btn_gestisci_prodotti.last.click()
        self.btn_deseleziona_tutti.click()
        self.btn_salva_prodotti.click()

        self.page.once("dialog", lambda dialog: dialog.accept())
        self.btn_elimina_categoria.last.click()