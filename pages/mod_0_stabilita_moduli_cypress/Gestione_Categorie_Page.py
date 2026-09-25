from playwright.async_api import Page
from pages.base_page import BasePage

class GestioneCat(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # --- CREA NUOVA CATEGORIA ---
        self.click_nuova_categoria = page.get_by_role("button", name="Nuova Categoria")
        self.campo_nome = page.get_by_role("textbox", name="Nome *")
        self.campo_descrizione = page.get_by_role("textbox", name="Descrizione")
        self.click_crea = page.get_by_role("button", name="Crea")

        # --- COMPLETA MODALE ---
        self.campo_ordine = page.get_by_role("spinbutton", name="Ordine")
        self.campo_icona = page.get_by_role("textbox", name="Icona")
        self.campo_colore = page.get_by_role("textbox", name="Colore")
        self.click_ultimo_crea = page.get_by_role("button", name="Salva Modifiche")

        # --- CATEGORIA PADRE (punto che crashava in Cypress) ---
        # A differenza di quanto skippato in Cypress, qui NON c'è ricerca
        # testuale: è un semplice v-select con lista fissa di opzioni.
        # Probabilmente il campo è stato semplificato proprio per eliminare
        # l'instabilità che causava lo skip originale. Nessun bisogno del
        # pattern anti-crash (.fill()) usato per Ricetta/Fornitori.
        self.trigger_categoria_padre = page.locator(
            ".v-input.v-input--horizontal.v-input--center-affix.v-input--density-default > .v-input__control > .v-field > .v-field__field > .v-field__input"
        )

    # --- NAVIGAZIONE ---
    def apri_catalogo(self):
        self.apri_gruppo_menu("Catalogo")
        self.naviga_a("/categories")

    # --- CREAZIONE CATEGORIA ---
    def apri_modale_categoria(self):
        self.click_nuova_categoria.click()

    def compila_categoria(self, dati_categoria: dict):
        self.campo_nome.fill(dati_categoria["nome_categoria"])
        self.campo_descrizione.fill(dati_categoria["descrizione"])
        

    def seleziona_categoria_padre_casuale(self):
        """Apre il dropdown 'Categoria Padre' e ne seleziona una a caso.

        NOTA: uso la versione con force=True (non _no_force). Il dropdown
        si trova dentro la modale "Nuova Categoria", il cui scrim di sfondo
        resta sempre visibile finché la modale è aperta (comportamento
        corretto, non un bug) — _no_force chiama internamente
        _attendi_scomparsa_scrim() e andrebbe quindi sempre in timeout in
        questo contesto. La versione con force salta quel controllo.
        """
        self.seleziona_option_casuale_dropdown(self.trigger_categoria_padre)

    def crea_categoria(self):
        self.click_crea.click()

    def compila_modulo_post(self,dati_categoria:dict):
        self.campo_ordine.fill(str(dati_categoria["ordine"]))
        self.campo_icona.fill(dati_categoria["icona"])
        self.campo_colore.fill(dati_categoria["colore"])
        self.click_ultimo_crea.click()
        