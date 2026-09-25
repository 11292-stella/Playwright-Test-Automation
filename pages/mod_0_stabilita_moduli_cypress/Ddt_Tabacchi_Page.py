from playwright.async_api import Page
from pages.base_page import BasePage

class DdtTabacchi(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # --- NAVIGAZIONE (qui cambia rispetto agli altri moduli: sottomenu
        # Catalogo > Tabacchi con role="option", non apri_gruppo_menu + naviga_a) ---
        self.opzione_catalogo = page.get_by_role("option", name="Catalogo")
        self.opzione_tabacchi = page.get_by_role("option", name="Tabacchi")
        self.link_ddt_fornitore = page.get_by_role("link", name="DDT Fornitore")

        # --- NUOVO DDT DA ORDINE ---
        self.click_nuovo_ddt_da_ordine = page.get_by_role("button", name="Nuovo DDT da Ordine")

        # --- RICERCA ORDINE/FORNITORE (stesso problema visto in Ricetta_Page:
        # Codegen punta a ".v-field__input" (contenitore visivo Vuetify), non
        # all'<input> reale annidato dentro. Invece di copiare la catena di
        # classi completa generata da Codegen (fragile: cambia con
        # density/theme/locale), restringiamo lo scope a
        # ".v-card-text .v-autocomplete input") ---
        self.campo_ricerca_ordine = page.locator(".v-card-text .v-autocomplete input")
        

    # --- NAVIGAZIONE ---
    def apri_catalogo_tabacchi_ddt(self):
        self.opzione_catalogo.click()
        self.opzione_tabacchi.click()
        self.link_ddt_fornitore.click()

    # --- APERTURA MODALE ---
    def apri_modale_nuovo_ddt_da_ordine(self):
        self.click_nuovo_ddt_da_ordine.click()

    # --- RICERCA E SELEZIONE ORDINE/FORNITORE ---
    def cerca_e_seleziona_ordine(self, testo_ricerca: str):
        """Cerca l'ordine per codice/fornitore e lo seleziona dal menu a tendina.

        testo_ricerca es. "TAB260706-007 — Dickens-Davis"
        """
        self.campo_ricerca_ordine.click()
        self.campo_ricerca_ordine.fill(testo_ricerca)

        opzione = self.page.get_by_text(testo_ricerca)
        opzione.wait_for(state="visible")
        opzione.click()
        

    