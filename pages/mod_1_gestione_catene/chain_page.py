from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class ChainPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        
        # --- NAVIGAZIONE & TABELLA ---
        self.menu_gestione_catene = page.get_by_text("Gestione catene", exact=True)
        self.link_registro_catene = page.get_by_role("link", name="Registro Catene")
        
        # --- BOTTONI CREAZIONE ---
        self.btn_nuova_catena = page.get_by_role("button", name="NUOVA CATENA")
        self.btn_crea = page.get_by_role("button", name="CREA")
        
        # --- FORM CREAZIONE ---
        self.input_slug = page.get_by_role("textbox", name="Slug (es. nord)")
        self.input_nome = page.get_by_role("textbox", name="Nome catena")
        self.input_max_negozi = page.get_by_role("spinbutton", name="Max negozi (default 100)")
        self.trigger_dropdown_gdpr = ".v-input.v-input--horizontal.v-input--density-comfortable .mdi-menu-down"
        
        # --- TABELLA E CANCELLAZIONE ---
        self.input_ricerca = page.get_by_placeholder("Cerca...")
        
        # --- MODALE GESTISCI NEGOZI ---
        self.dropdown_aggiungi_negozio = page.get_by_role("combobox", name="Aggiungi negozio")
        self.btn_aggiungi_negozio = page.get_by_role("button", name="AGGIUNGI")
        self.btn_chiudi_modale_negozi = page.get_by_role("button", name="CHIUDI")

    def apri_modulo_catene(self):
        """Naviga fino al modulo Registro Catene."""
        self.assicura_sidebar_aperta()
        self.menu_gestione_catene.click()
        self.link_registro_catene.click()
        expect(self.btn_nuova_catena).to_be_visible()

    def apri_form_nuova_catena(self):
        """Apre la modale di creazione."""
        self.btn_nuova_catena.click()

    def compila_form_catena(self, dati_catena: dict):
        """Compila i campi del form, seleziona la tendina e invia i dati."""
        self.input_slug.fill(dati_catena["slug"])
        self.input_nome.fill(dati_catena["nome"])
        self.input_max_negozi.fill(dati_catena["max_negozi"])
        self.seleziona_option_casuale_dropdown(self.trigger_dropdown_gdpr)
        self.btn_crea.click()

    def cerca_catena(self, testo_ricerca: str):
        """Filtra la tabella digitando il testo nella barra di ricerca.

        Se il testo è nel formato "Nome (slug)" (usato per identificare le
        catene di test nei metodi che gestiscono negozi/associazioni), la
        ricerca viene fatta solo sul nome: il campo di ricerca del backend
        non supporta la stringa combinata con lo slug tra parentesi e
        restituirebbe zero risultati.
        """
        nome_ricerca = testo_ricerca.split(" (")[0]
        if self.input_ricerca.is_visible():
            self.input_ricerca.fill(nome_ricerca)
            self.page.wait_for_timeout(500)

    def elimina_catena(self, nome_catena: str):
        """Cerca la riga della catena ed esegue l'eliminazione confermando il pop-up nativo."""
        self.cerca_catena(nome_catena)
        self.page.once("dialog", lambda dialog: dialog.accept())

        riga_catena = self.page.locator("tbody tr").filter(has_text=nome_catena)
        riga_catena.get_by_title("Elimina").click()

        self.page.wait_for_timeout(1000)
        expect(riga_catena).not_to_be_visible()

    # --- GESTIONE E ASSOCIAZIONE NEGOZI ---

    def apri_gestione_negozi(self, nome_catena: str):
        """Trova la riga della catena e clicca sul bottone 'Gestisci negozi'.

        NOTA: la tabella mostra nome e Chain ID in due celle separate, senza
        il formato "Nome (slug)" usato altrove (es. nelle dropdown) per
        identificare le catene di test. Se nome_catena arriva in quel
        formato combinato, va quindi ripulito prima di essere usato per
        cercare/filtrare, altrimenti il filtro non trova mai la riga (il
        testo con "(...)" non esiste da nessuna parte nel DOM).

        NOTA 2: nelle tabelle Vuetify le icone azione per riga sono spesso
        visibili solo in hover (opacity/display gestiti via CSS al passaggio
        del mouse sulla riga). Playwright non genera un hover reale prima
        del click, quindi se il bottone resta non interagibile finché la
        riga non riceve l'hover, il click va in timeout pur essendo la riga
        correttamente trovata. Forziamo quindi un hover esplicito sulla riga
        prima di cliccare l'icona.
        """
        nome_pulito = nome_catena.split(" (")[0]
        self.cerca_catena(nome_pulito)

        riga = self.page.locator("tbody tr").filter(has_text=nome_pulito)
        expect(riga).to_be_visible(timeout=10000)

        self._scrolla_al_centro(riga)
        riga.hover()

        btn_gestisci = riga.get_by_title("Gestisci negozi")
        btn_gestisci.wait_for(state="visible", timeout=5000)
        btn_gestisci.click()

        expect(self.btn_chiudi_modale_negozi).to_be_visible()

    def rimuovi_negozio_se_presente(self, nome_negozio: str):
        """
        Controlla se il negozio è presente nei negozi associati (lista .v-card).
        Se lo trova, lo rimuove e attende che scompaia per riabilitare l'opzione nella tendina.
        """
        item_negozio = self.page.locator(".v-card .v-list-item").filter(has_text=nome_negozio)
        
        # Breve attesa per il rendering dinamico della modale
        self.page.wait_for_timeout(500)
        
        if item_negozio.count() > 0 and item_negozio.first.is_visible():
            # Selettore univoco per il pulsante rosso presente nella parte destra della riga
            btn_rimuovi = item_negozio.locator(".v-list-item__append button")
            btn_rimuovi.click()
            
            # Attende la scomparsa dell'elemento
            expect(item_negozio).not_to_be_visible()
            self.page.wait_for_timeout(500)

    def associa_negozio_a_catena(self, nome_negozio: str):
        """Seleziona il negozio dalla tendina e clicca su AGGIUNGI.

        NOTA: usiamo il locator per ruolo/nome accessibile
        (get_by_role("combobox", name="Aggiungi negozio")) invece del
        selettore CSS generico usato in precedenza (".v-card .v-autocomplete
        .v-field"): quest'ultimo, essendo troppo generico, poteva matchare
        un elemento diverso da quello atteso (es. un altro .v-card/.v-field
        presente in pagina) e il click(force=True) non apriva affatto il
        menu, causando timeout sull'attesa della prima opzione.

        NOTA 2: a differenza delle altre dropdown del progetto, qui NON
        usiamo seleziona_option_per_testo_dropdown (che fa match
        exact=True): il testo dell'opzione include anche lo slug del
        negozio tra parentesi (es. "Bistrot Demo (reseller_demo_...)"),
        dinamico e non prevedibile a priori, quindi un match esatto su
        "Bistrot Demo" da solo non troverebbe mai l'opzione. Usiamo un match
        non esatto (substring) sul nome del negozio.
        """
        self.dropdown_aggiungi_negozio.click()

        opzioni = self.page.locator(".v-overlay-container [role='option']")
        opzioni.first.wait_for(state="visible")
        self.page.get_by_role("option", name=nome_negozio).click()

        # Clicca su AGGIUNGI
        self.btn_aggiungi_negozio.click()
        
        # Piccola attesa per il rendering del nuovo item aggiunto
        self.page.wait_for_timeout(500)

    def verifica_negozio_associato(self, nome_negozio: str):
        """Verifica che il negozio compaia nella lista dei negozi associati della modale."""
        item_negozio = self.page.locator(".v-card .v-list-item").filter(has_text=nome_negozio)
        expect(item_negozio).to_be_visible()

    def chiudi_modale_negozi(self):
        """Chiude la modale 'Negozi di...'."""
        self.btn_chiudi_modale_negozi.click()