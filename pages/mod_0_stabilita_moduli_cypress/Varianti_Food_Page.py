from playwright.async_api import Page
from pages.base_page import BasePage

class Varianti(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # --- APRI NUOVO PRODOTTO ---
        self.click_nuovo_prodotto = page.get_by_role("button", name="Nuovo Prodotto")
        self.click_tab_varianti = page.get_by_role("tab", name="Varianti Food")
        self.click_assegna_gruppo = page.get_by_role("button", name="Assegna Gruppo")

        # --- RICERCA GRUPPO CRASH ---
        self.seleziona_gruppo = page.locator(
            ".v-field.v-field--appended.v-field--center-affix.v-field--prepended.v-field--variant-filled"
        ).last.locator("input")

        self.assegna_gruppo = page.get_by_role("button", name="Assegna", exact=True)
        self.crea_prodotto = page.get_by_role("button", name="Crea Prodotto")

        # --- NAVIGAZIONE ---
    def apri_catalogo(self):
            self.apri_gruppo_menu("Catalogo")
            self.naviga_a("/products")

     # --- CREAZIONE PRODOTTO ---
    def apri_modale_prodotto(self):
            self.click_nuovo_prodotto.click()
            self.click_tab_varianti.click()
            self.click_assegna_gruppo.click()

    def cerca_e_seleziona_gruppo(self, nome_gruppo:str):
          self.seleziona_gruppo.click()
          self.seleziona_gruppo.fill(nome_gruppo)

          opzione = self.page.get_by_text(nome_gruppo)
          opzione.wait_for(state="visible")
          opzione.click()

          self.assegna_gruppo.click()
          self.crea_prodotto.click()




