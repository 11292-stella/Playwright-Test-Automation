from playwright.async_api import Page
from pages.base_page import BasePage

class Ricetta(BasePage):
    def __init__(self, page:Page):
        super().__init__(page)

        # --- CREA NUOVO PRODOTTO
        self.click_nuovo_prodotto = page.get_by_role("button", name="Nuovo Prodotto")
        self.apri_tab_ricetta = page.get_by_role("tab", name="Ricetta")
        self.aggiungi_ingrediente = page.get_by_role("button", name="Aggiungi Ingrediente").first

        # --- RICERCA INGREDIENTE (punto che crashava in Cypress) ---
        # Selettore preso da Codegen, poi corretto: Codegen puntava al div
        # .v-field__input (contenitore visivo Vuetify), non all'<input>
        # vero e proprio annidato dentro — .fill() infatti falliva con
        # "Element is not an <input>...". Aggiungiamo "input" per prendere
        # l'elemento editabile reale. .last perché ad ogni "Aggiungi
        # Ingrediente" viene aggiunta una nuova riga con un campo identico.
        self.campo_ricerca_ingrediente = page.locator(
            ".v-field.v-field--appended.v-field--center-affix.v-field--prepended.v-field--variant-filled"
        ).last.locator("input")

        # --- DATI INGREDIENTE ---
        self.quantita_ingrediente = page.get_by_role("spinbutton", name="Quantità")
        self.salva_ingrediente = page.get_by_role("button", name="Aggiungi", exact=True)

        # --- MODULO SOTTOSTANTE ---
        self.resa_ricetta = page.get_by_role("spinbutton", name="Resa")
        self.tempo_ricetta = page.get_by_role("spinbutton", name="Tempo Preparazione")
        self.descrizione_ricetta = page.get_by_role("textbox", name="Istruzioni di preparazione")
        self.crea_ricetta_completa = page.get_by_role("button", name="Crea Prodotto")

    # --- NAVIGAZIONE ---
    def apri_catalogo(self):
        self.apri_gruppo_menu("Catalogo")
        self.naviga_a("/products")


    # --- CREAZIONE PRODOTTO ---
    def apri_modale_prodotto(self):
        self.click_nuovo_prodotto.click()

    # --- CLICK TAB RICETTA ---
    def tab_ricetta(self):
        self.apri_tab_ricetta.click()
        self.aggiungi_ingrediente.click()

    # --- RICERCA E SELEZIONE INGREDIENTE ---
    def cerca_e_seleziona_ingrediente(self, nome_ingrediente: str):
        """Cerca un ingrediente per nome/SKU e lo seleziona dal menu a tendina.

        NOTA ANTI-CRASH (bug noto in Cypress): la selezione ingrediente
        triggera 3 chiamate API simultanee (categories/uom/allergens meta)
        che in Cypress causavano crash intermittente del renderer quando si
        digitava carattere per carattere con cy.type(). Il fix validato in
        Cypress è stato passare a invoke("val", term).trigger("input"):
        imposta il valore in un colpo solo e dispara UN SOLO evento
        'input', invece di uno per ogni tasto premuto.

        page.fill() di Playwright fa esattamente questo di default (setta
        il valore e dispara un solo evento 'input'/'change'), quindi
        partiamo già con il pattern corretto, senza bisogno del workaround
        che era servito in Cypress.
        """
        self.campo_ricerca_ingrediente.click()
        self.campo_ricerca_ingrediente.fill(nome_ingrediente)

        opzione = self.page.get_by_text(nome_ingrediente)
        opzione.wait_for(state="visible")
        opzione.click()

    def compila_dati_ingrediente_selezionato(self, dati_ingrediente:dict):
        self.quantita_ingrediente.fill(str(dati_ingrediente["quantita"]))
        self.salva_ingrediente.click()

    def compila_modulo_sottostante_ricetta(self,dati_ingredienti: dict):
        self.resa_ricetta.fill(str(dati_ingredienti["resa_ricetta"]))
        self.tempo_ricetta.fill(str(dati_ingredienti["tempo_ricetta"]))
        self.descrizione_ricetta.fill(dati_ingredienti["descrizione_ricetta"])
        self.crea_ricetta_completa.click()

    