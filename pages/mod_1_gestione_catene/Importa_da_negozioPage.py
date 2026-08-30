from playwright.sync_api import Page, expect
from pages.base_page import BasePage
import random
import re

class ImportaDA(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # --- ELEMENTI IMPORTA DA ---
        self.importa_da_catena = page.get_by_label("Catena")

        # --- RICERCA ELEMENTI ---
        self.negozio_sorgente = page.get_by_role("combobox", name="Negozio da cui leggere il")
        self.click_anteprima = page.get_by_role("button", name="Analizza (anteprima)")
        self.click_importa_in_catena = page.get_by_role("button", name=re.compile(r"^Importa in catena"))
        self.click_vai_al_catalogo = page.get_by_role("button", name="Vai a Catalogo Catena")


        # --- CHECKBOX SEZIONI DA IMPORTARE ---
        self.checkbox_prodotti_bom = page.get_by_role("checkbox", name="Prodotti (con ricette/BOM)")

        self.checkbox_sezioni_import = [
            page.get_by_role("checkbox", name="Reparti fiscali"),
            page.get_by_role("checkbox", name="Categorie", exact=True),
            page.get_by_role("checkbox", name="Ingredienti"),
            page.get_by_role("checkbox", name="Listini"),
            page.get_by_role("checkbox", name="Layout cassa"),
            page.get_by_role("checkbox", name="Config stampa"),
            page.get_by_role("checkbox", name="Righe listino"),
            page.get_by_role("checkbox", name="Fornitori"),
            page.get_by_role("checkbox", name="Varianti", exact=True),
            page.get_by_role("checkbox", name="Reparti di vendita"),
            page.get_by_role("checkbox", name="Categorie ingrediente"),
            page.get_by_role("checkbox", name="Gruppi varianti"),
            self.checkbox_prodotti_bom,
            page.get_by_role("checkbox", name="Contratti fornitore"),
            page.get_by_role("checkbox", name="Regole stampa auto"),
        ]

        # Sezioni ammesse per la selezione casuale: esclude "Prodotti (con ricette/BOM)"
        # perché importa troppi dati e appesantisce il test.
        self.checkbox_sezioni_selezionabili = [
            c for c in self.checkbox_sezioni_import if c != self.checkbox_prodotti_bom
        ]


    # --- NAVIGAZIONE ---
    def apri_catalogo(self):
            """Naviga fino a Clienti Catena (Gestione catene > importa_da_negozio)."""
            self.apri_gruppo_menu("Gestione catene")
            self.naviga_a("/chain-catalog-import")

      # --- AZIONI ---
    def filtra_per_catena(self, nome_catena: str):
             """Seleziona una catena specifica dal filtro."""
             self.seleziona_option_per_testo_dropdown(self.importa_da_catena, nome_catena)
             self.attendi_scomparsa_loader()

    def cerca_negozio(self, nome_negozio: str):
          """Seleziona il negozio sorgente dalla tendina.

          NOTA: come in associa_negozio_a_catena (chain_page.py), qui NON
          usiamo seleziona_option_per_testo_dropdown perché fa match
          exact=True: il testo dell'opzione include anche lo slug del
          negozio tra parentesi (es. "Bistrot Demo (reseller_demo_...)"),
          dinamico e non prevedibile a priori, quindi un match esatto su
          "Bistrot Demo" da solo non troverebbe mai l'opzione. Apriamo la
          tendina e usiamo un match non esatto (substring) sul nome.
          """
          self.negozio_sorgente.click()

          opzioni = self.page.locator(".v-overlay-container [role='option']")
          opzioni.first.wait_for(state="visible")
          self.page.get_by_role("option", name=nome_negozio).click()

    def deseleziona_tutte_le_sezioni(self):
          """Deseleziona tutte le checkbox delle sezioni da importare."""
          for checkbox in self.checkbox_sezioni_import:
                if checkbox.is_checked():
                      checkbox.uncheck()

    def seleziona_sezione_casuale(self):
          """Deseleziona tutte le sezioni e ne seleziona una sola a caso
          (esclusa 'Prodotti (con ricette/BOM)', vedi checkbox_sezioni_selezionabili)."""
          self.deseleziona_tutte_le_sezioni()
          random.choice(self.checkbox_sezioni_selezionabili).check()

    def click_analizza_anteprima(self):
          self.click_anteprima.click()
          self.attendi_scomparsa_loader()

    def controlla_e_importa(self):
          """Legge il numero tra parentesi sul bottone 'Importa in catena (N)'.
          Se N è 0 (nulla da importare per la sezione selezionata, scelta a
          caso da seleziona_sezione_casuale) è uno stato legittimo, non un
          bug: il test si conclude qui senza cliccare importa/vai al
          catalogo, ma termina come PASSED (non fallito né skippato).
          Altrimenti clicca 'Importa in catena' e poi 'Vai a Catalogo
          Catena' per confermare l'esito."""
          testo_bottone = self.click_importa_in_catena.inner_text()
          match = re.search(r"\((\d+)\)", testo_bottone)
          numero_elementi = int(match.group(1)) if match else 0

          if numero_elementi == 0:
                print(f"Nessun elemento da importare per la sezione selezionata (bottone: '{testo_bottone}'), nulla da fare.")
                return

          self.click_importa_in_catena.click()
          self.attendi_scomparsa_loader()
          self.click_vai_al_catalogo.click()