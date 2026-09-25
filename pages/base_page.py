import random
import re
from playwright.sync_api import Page, expect, TimeoutError as PlaywrightTimeoutError


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    # --- GESTIONE NAVIGAZIONE MODULI ---

    def naviga_a(self, href: str, verifica_url: bool = True, timeout: int = 10000):
        """
        Naviga cliccando un link di menu (top-level o dentro un sottomenu),
        identificato dal suo href. Riusabile per cambio modulo o navigazione
        interna a un modulo (es. sottomenu "Gestione catene").

        :param href: path dell'href del link, es. "/chain-dashboard"
        :param verifica_url: se True, aspetta che l'URL contenga l'href dato
        :param timeout: timeout in ms per l'attesa dell'URL
        """
        link = self.page.locator(f'a[href="{href}"]')
        expect(link).to_be_visible(timeout=timeout)
        link.click()

        if verifica_url:
            expect(self.page).to_have_url(re.compile(re.escape(href)), timeout=timeout)

        self.attendi_scomparsa_loader()

    def apri_gruppo_menu(self, nome_gruppo: str):
        """
        Espande un gruppo di menu nella sidebar (es. 'Gestione catene')
        se non è già aperto. Necessario prima di navigare a un link
        dentro quel sottomenu.
        """
        self.assicura_sidebar_aperta()
        gruppo = self.page.get_by_text(nome_gruppo, exact=True)
        # v-list-group ha aria-expanded sul trigger, controlliamo lo stato
        if gruppo.get_attribute("aria-expanded") != "true":
            gruppo.click()

    # --- GESTIONE DRAWER / SIDEBAR VUETIFY ---

    def assicura_sidebar_aperta(self):
        """Verifica lo stato del drawer Vuetify e lo apre solo se è chiuso o compresso."""
        drawer = self.page.locator(".v-navigation-drawer")
        classi_drawer = drawer.get_attribute("class") or ""

        if "v-navigation-drawer--close" in classi_drawer or "v-navigation-drawer--rail" in classi_drawer:
            self.page.locator(".v-app-bar-nav-icon").click()

    # --- GESTIONE DROPDOWN / SELECT VUETIFY ---

    def _risolvi_trigger(self, trigger):
        """Helper interno: accetta sia una stringa CSS che un Locator già costruito
        (es. page.get_by_label(...)) e restituisce sempre un Locator."""
        return self.page.locator(trigger) if isinstance(trigger, str) else trigger

    def _attendi_scomparsa_scrim(self, timeout: int = 5000):
        """Attende che eventuali scrim (overlay di sfondo) di menu Vuetify
        precedenti siano completamente scomparsi prima di interagire.
        Necessario perché un click su un trigger può fallire con
        'subtree intercepts pointer events' se lo scrim di un menu
        aperto/chiuso in precedenza è ancora in fase di transizione."""
        scrim = self.page.locator(".v-overlay__scrim")
        if scrim.count() > 0:
            scrim.last.wait_for(state="hidden", timeout=timeout)

    def _scrolla_al_centro(self, locator):
        """Scrolla l'elemento al centro verticale della viewport (invece del
        default 'nearest' usato da Playwright), per evitare che finisca
        coperto da elementi sticky come l'header/toolbar in alto."""
        locator.evaluate("el => el.scrollIntoView({block: 'center', behavior: 'instant'})")

    def seleziona_option_casuale_dropdown(self, trigger):
        """Apre una dropdown Vuetify tramite il suo trigger (stringa CSS o Locator)
        e seleziona un'opzione casuale. Click forzato: usa questa versione quando
        un elemento decorativo (es. v-field__input) copre il vero target cliccabile."""
        trigger_locator = self._risolvi_trigger(trigger)
        trigger_locator.click(force=True)

        opzioni = self.page.locator(".v-overlay-container [role='option']")
        opzioni.first.wait_for(state="visible")

        count = opzioni.count()
        if count > 0:
            indice_casuale = random.randint(0, count - 1)
            opzioni.nth(indice_casuale).click()

    def seleziona_option_per_testo_dropdown(self, trigger, testo_opzione: str):
        """Apre una dropdown Vuetify (trigger: stringa CSS o Locator) e seleziona
        un'opzione specifica basandosi sul testo. Click forzato: usa questa versione
        quando un elemento decorativo (es. v-field__input) copre il vero target cliccabile.

        NOTA: usa get_by_role(..., exact=True) invece di filter(has_text=...) perché
        has_text fa match a substring (es. "Testo" matcherebbe anche "Testo lungo",
        "Data" matcherebbe anche "Data e ora"), causando strict mode violation quando
        più opzioni condividono un prefisso testuale.
        """
        trigger_locator = self._risolvi_trigger(trigger)
        trigger_locator.click(force=True)

        opzioni = self.page.locator(".v-overlay-container [role='option']")
        opzioni.first.wait_for(state="visible")
        self.page.get_by_role("option", name=testo_opzione, exact=True).click()

    def seleziona_option_casuale_dropdown_no_force(self, trigger):
        """Come seleziona_option_casuale_dropdown, ma con click 'normale' (senza force).
        Usa questa versione quando il click forzato non attiva correttamente
        l'apertura del menu (es. dropdown 'Modello' in Fatturazione Catena)."""
        trigger_locator = self._risolvi_trigger(trigger)
        self._attendi_scomparsa_scrim()
        self._scrolla_al_centro(trigger_locator)
        trigger_locator.click()

        opzioni = self.page.locator(".v-overlay-container [role='option']")
        opzioni.first.wait_for(state="visible")

        count = opzioni.count()
        if count > 0:
            indice_casuale = random.randint(0, count - 1)
            opzioni.nth(indice_casuale).click()

    def seleziona_option_per_testo_dropdown_no_force(self, trigger, testo_opzione: str):
        """Come seleziona_option_per_testo_dropdown, ma con click 'normale' (senza force).
        Usa questa versione quando il click forzato non attiva correttamente
        l'apertura del menu (es. dropdown 'Modello' in Fatturazione Catena).

        Prima del click:
        - attende che eventuali scrim di overlay precedenti siano scomparsi
          (evita 'v-overlay__scrim ... subtree intercepts pointer events')
        - scrolla l'elemento al centro della viewport (evita che finisca
          coperto dalla toolbar sticky in alto, causa di retry infiniti)

        NOTA: usa get_by_role(..., exact=True) invece di filter(has_text=...) per lo
        stesso motivo di seleziona_option_per_testo_dropdown (evitare match a substring).
        """
        trigger_locator = self._risolvi_trigger(trigger)
        self._attendi_scomparsa_scrim()
        self._scrolla_al_centro(trigger_locator)
        trigger_locator.click()

        opzioni = self.page.locator(".v-overlay-container [role='option']")
        opzioni.first.wait_for(state="visible")
        self.page.get_by_role("option", name=testo_opzione, exact=True).click()

    def seleziona_option_per_testo_dropdown_icona(self, trigger, testo_opzione: str):
        """Apre una dropdown Vuetify cliccando sulla freccina del campo
        (icona 'mdi-menu-down') invece che sull'input o sul testo del valore
        corrente. Una registrazione con Playwright Codegen su questo stesso
        form ha confermato che l'icona è il target davvero affidabile:
        l'input/testo del valore vengono spesso coperti da scrim, overlay
        residui o dalla toolbar sticky in alto, mentre l'icona resta
        cliccabile in modo consistente.
        Usa questa versione quando anche seleziona_option_per_testo_dropdown_no_force
        continua a fallire con 'subtree intercepts pointer events'
        (es. dropdown 'Modello'/'Ciclo' in Fatturazione Catena).

        NOTA: usa get_by_role(..., exact=True) invece di filter(has_text=...) per lo
        stesso motivo di seleziona_option_per_testo_dropdown (evitare match a substring).

        :param trigger: Locator dell'input del campo, es. page.get_by_label("Modello").
                         Deve essere l'input dentro il contenitore Vuetify ".v-field".
        """
        trigger_locator = self._risolvi_trigger(trigger)
        self._attendi_scomparsa_scrim()

        campo = trigger_locator.locator(
            "xpath=ancestor::div[contains(concat(' ', normalize-space(@class), ' '), ' v-field ')][1]"
        )
        icona = campo.locator(".mdi-menu-down")
        self._scrolla_al_centro(icona)
        icona.click()

        opzioni = self.page.locator(".v-overlay-container [role='option']")
        opzioni.first.wait_for(state="visible")
        self.page.get_by_role("option", name=testo_opzione, exact=True).click()

    def cicla_tutte_le_opzioni_dropdown(self, trigger):
        """Apre una dropdown Vuetify (tramite l'icona 'mdi-menu-down', lo stesso
        pattern affidabile di seleziona_option_per_testo_dropdown_icona) e clicca
        in sequenza TUTTE le opzioni disponibili, in ordine casuale. L'ultima
        cliccata resta selezionata: il risultato finale è quindi un'opzione
        casuale, ma nel frattempo abbiamo 'esercitato' ogni valore del dropdown.

        Utile per verificare che ogni opzione sia effettivamente selezionabile
        (es. dropdown 'Tipo Prodotto' con Kit, Servizio, Merce, Bevanda, Piatto,
        Materia Prima...) prima di lasciarne una a caso per il resto del test.

        NOTA: non usa _attendi_scomparsa_scrim perché se il dropdown si trova
        dentro una modale (es. modale 'Nuovo Prodotto'), lo scrim di sfondo
        della modale resta sempre visibile finché la modale è aperta, quindi
        l'attesa andrebbe in timeout. Usiamo invece la comparsa/scomparsa
        della lista di opzioni stessa per sincronizzarci con l'apertura e
        la chiusura del menu.

        :param trigger: Locator dell'input del campo, es. page.get_by_label("Tipo Prodotto").
                         Deve essere l'input dentro il contenitore Vuetify ".v-field".
        """
        trigger_locator = self._risolvi_trigger(trigger)

        campo = trigger_locator.locator(
            "xpath=ancestor::div[contains(concat(' ', normalize-space(@class), ' '), ' v-field ')][1]"
        )
        icona = campo.locator(".mdi-menu-down")
        opzioni = self.page.locator(".v-overlay-container [role='option']")

        # Primo giro: apriamo il menu solo per leggere tutte le opzioni disponibili
        self._scrolla_al_centro(icona)
        icona.click()
        opzioni.first.wait_for(state="visible")
        testi_opzioni = opzioni.all_inner_texts()
        self.page.keyboard.press("Escape")  # chiudiamo senza selezionare nulla
        opzioni.first.wait_for(state="hidden")

        # Mescoliamo l'ordine: così l'ultima cliccata (quella che resta
        # selezionata alla fine) è casuale
        random.shuffle(testi_opzioni)

        for testo in testi_opzioni:
            icona.click()
            opzioni.first.wait_for(state="visible")
            self.page.get_by_role("option", name=testo, exact=True).click()
            opzioni.first.wait_for(state="hidden")

    # --- UTILITY GENERALI VUETIFY ---

    def attendi_scomparsa_loader(self, timeout: int = 5000):
        """Attende che eventuali spinner/progress-bar di Vuetify abbiano finito.
        Itera sui singoli elementi trovati per evitare strict mode violation
        quando ce n'è più di uno in pagina (es. loader decorativi nei v-field).

        NOTA: alcune pagine (es. /products) hanno più widget indipendenti,
        ognuno col proprio spinner. Se uno di questi resta appeso perché la
        sua chiamata API non risponde mai (stesso comportamento osservato
        anche in Cypress sull'endpoint dashboard/stats, che a volte non
        restituisce risposta), non deve bloccare l'intero test: ogni loader
        ha quindi un timeout ridotto (5s invece del default 30s) e, se
        allo scadere è ancora visibile, viene ignorato — il contenuto
        principale della pagina è comunque già pronto a quel punto.
        """
        loaders = self.page.locator(".v-progress-linear, .v-progress-circular")
        for loader in loaders.all():
            try:
                loader.wait_for(state="hidden", timeout=timeout)
            except PlaywrightTimeoutError:
                pass

    def clicca_e_attendi_risposta(self, trigger, url_pattern, timeout: int = 10000):
        """Clicca un elemento e attende la risposta di rete corrispondente,
        invece di affidarsi solo alla scomparsa di uno spinner/loader.

        L'auto-waiting di Playwright verifica lo stato dell'elemento (visibile,
        stabile, non coperto, ecc.) prima del click, ma NON aspetta le chiamate
        API in automatico: quello va sincronizzato esplicitamente. Usa questo
        metodo al posto di un semplice click + attendi_scomparsa_loader quando
        serve la certezza che la richiesta sia davvero completata (es. un
        salvataggio il cui loader potrebbe essere troppo rapido da intercettare,
        o quando serve controllare l'esito della risposta).

        :param trigger: stringa CSS o Locator dell'elemento da cliccare
        :param url_pattern: sottostringa o regex (re.compile) da matchare
                             nell'URL della risposta, es. "**/chain-billing/model"
                             o re.compile(r"/chain-billing/model$")
        :param timeout: timeout in ms per l'attesa della risposta
        :return: l'oggetto Response di Playwright (utile per controllare
                 status_code, response.json(), ecc.)
        """
        trigger_locator = self._risolvi_trigger(trigger)
        with self.page.expect_response(url_pattern, timeout=timeout) as response_info:
            trigger_locator.click()
        return response_info.value

    # --- GESTIONE CAMPI DATA ---

    def compila_data(self, trigger, data: str):
        """Compila un campo <input type="date"> Vuetify (stringa CSS o Locator).

        :param trigger: selettore CSS o Locator del campo data
        :param data: data nel formato "YYYY-MM-DD" (formato richiesto dagli
                     input HTML type="date", indipendentemente da come viene
                     mostrata a schermo, es. "03/07/2026" in italiano)
        """
        trigger_locator = self._risolvi_trigger(trigger)
        trigger_locator.fill(data)

        # --- DEBUG / DIAGNOSTICA ---

    def elenca_dropdown_pagina(self, selettore: str = ".v-select"):
        """Utility diagnostica: stampa indice, visibilità e testo di tutti gli
        elementi che matchano il selettore dato (default: tutti i .v-select
        nella pagina). Utile quando una pagina ha più dropdown Vuetify simili
        e serve capire quale indice/testo corrisponde a quello che si vuole
        automatizzare, prima di scrivere il locator definitivo nella page object.

        Lancia il test con -s per vedere l'output in console, es:
        pytest tests/percorso/test_x.py -s --headed

        :param selettore: selettore CSS degli elementi da ispezionare
        """
        elementi = self.page.locator(selettore)
        count = elementi.count()
        print(f"Trovati {count} elementi per '{selettore}':")

        for i in range(count):
            el = elementi.nth(i)
            try:
                visibile = el.is_visible()
                testo = el.inner_text()
            except Exception as e:
                visibile = "ERRORE"
                testo = str(e)
            print(f"  [{i}] visible={visibile} text={testo!r}")

    def dropdown_per_testo(self, testo_label: str, selettore: str = ".v-select"):
        """Restituisce l'input trigger del dropdown Vuetify il cui testo
        (label/valore visibile) contiene 'testo_label', invece di affidarsi
        alla posizione nel DOM (.first), che può puntare all'elemento
        sbagliato quando ci sono più dropdown simili nella stessa pagina.

        :param testo_label: testo (anche parziale) presente nel dropdown, es. "Categorie"
        :param selettore: selettore CSS del contenitore dropdown (default: .v-select)
        :return: Locator dell'input, pronto da passare a
                 seleziona_option_per_testo_dropdown_icona / _no_force / ecc.
        """
        return (
            self.page.locator(selettore)
            .filter(has_text=testo_label)
            .locator(".v-field__input")
        )

    def seleziona_opzione_casuale_tra_testi(self, testi_opzioni: list[str]):
        """Seleziona un'opzione casuale tra una lista di testi/opzioni già visibili
        in pagina (es. un gruppo di scelta tipo radio/chip, non un dropdown Vuetify
        con overlay). Usa get_by_text con exact=True per evitare match parziali
        tra opzioni con testo simile (es. "Solo email" vs "Solo email (magic link)").

        :param testi_opzioni: lista dei testi esatti tra cui scegliere,
                               es. ["Solo email (magic link)", "Solo telefono (OTP SMS)",
                                    "Entrambi (email + SMS)", "Nessuna (sconsigliato)"]
        """
        testo_scelto = random.choice(testi_opzioni)
        self.page.get_by_text(testo_scelto, exact=True).click()

        # --- GESTIONE DOWNLOAD FILE ---

    def clicca_e_scarica(self, trigger, cartella_destinazione: str = "downloads", timeout: int = 15000):
        """Clicca un elemento che avvia il download di un file (es. 'Scarica PDF')
        e salva il file scaricato in locale, senza mai far comparire il dialog
        nativo del sistema operativo 'Salva con nome'.

        NOTA: expect_download() intercetta l'evento di download del browser
        PRIMA che il sistema operativo apra qualsiasi finestra di salvataggio,
        quindi il file viene scaricato automaticamente in background. Se il tuo
        browser continua ad aprire il dialog nativo, controlla le impostazioni
        di Chrome: "Chiedi dove salvare ogni file prima di scaricarlo" deve
        essere disattivato per il profilo usato da Playwright.

        :param trigger: stringa CSS o Locator del bottone/link che avvia il download
        :param cartella_destinazione: cartella locale dove salvare il file
                                       (creata automaticamente se non esiste)
        :param timeout: timeout in ms per l'attesa dell'evento di download
        :return: percorso completo del file salvato
        """
        import os

        trigger_locator = self._risolvi_trigger(trigger)
        os.makedirs(cartella_destinazione, exist_ok=True)

        with self.page.expect_download(timeout=timeout) as download_info:
            trigger_locator.click()
        download = download_info.value

        percorso_file = os.path.join(cartella_destinazione, download.suggested_filename)
        download.save_as(percorso_file)
        return percorso_file

    
    def seleziona_prima_opzione_dropdown_icona(self, trigger):
        """Come seleziona_option_per_testo_dropdown_icona, ma seleziona sempre
        la prima opzione disponibile invece di cercarne una per testo. Utile
        quando l'opzione dipende da dati creati da un altro modulo (es.
        'Segmento destinatari' dipende dai segmenti creati in precedenza) e
        non serve conoscere il nome esatto.

        :param trigger: Locator dell'input del campo, es. page.get_by_label("Segmento destinatari").
                        Deve essere l'input dentro il contenitore Vuetify ".v-field".
        """
        trigger_locator = self._risolvi_trigger(trigger)
        self._attendi_scomparsa_scrim()

        campo = trigger_locator.locator(
            "xpath=ancestor::div[contains(concat(' ', normalize-space(@class), ' '), ' v-field ')][1]"
        )
        icona = campo.locator(".mdi-menu-down")
        self._scrolla_al_centro(icona)
        icona.click()

        opzioni = self.page.locator(".v-overlay-container [role='option']")
        opzioni.first.wait_for(state="visible")
        opzioni.first.click()

    def seleziona_option_per_testo_dropdown_in_modale(self, trigger, testo_opzione: str):
        """Come seleziona_option_per_testo_dropdown_icona, ma senza attendere
        la scomparsa dello scrim: usa questa versione quando il dropdown si
        trova dentro una modale (es. 'Importa da categoria prodotti' nella
        modale 'Nuova Categoria'), perché lo scrim della modale resta sempre
        visibile finché la modale è aperta e l'attesa andrebbe in timeout.
        Stesso pattern di sincronizzazione usato in cicla_tutte_le_opzioni_dropdown.
        """
        trigger_locator = self._risolvi_trigger(trigger)

        campo = trigger_locator.locator(
            "xpath=ancestor::div[contains(concat(' ', normalize-space(@class), ' '), ' v-field ')][1]"
        )
        icona = campo.locator(".mdi-menu-down")
        self._scrolla_al_centro(icona)
        icona.click()

        opzioni = self.page.locator(".v-overlay-container [role='option']")
        opzioni.first.wait_for(state="visible")
        self.page.get_by_role("option", name=testo_opzione, exact=True).click()

    def seleziona_option_casuale_dropdown_icona(self, trigger):
        """Come seleziona_prima_opzione_dropdown_icona, ma seleziona un'opzione
        casuale invece della prima."""
        trigger_locator = self._risolvi_trigger(trigger)
        self._attendi_scomparsa_scrim()

        campo = trigger_locator.locator(
            "xpath=ancestor::div[contains(concat(' ', normalize-space(@class), ' '), ' v-field ')][1]"
        )
        icona = campo.locator(".mdi-menu-down")
        self._scrolla_al_centro(icona)
        icona.click()

        opzioni = self.page.locator(".v-overlay-container [role='option']")
        opzioni.first.wait_for(state="visible")

        count = opzioni.count()
        if count > 0:
            indice_casuale = random.randint(0, count - 1)
            opzioni.nth(indice_casuale).click()

    def seleziona_option_casuale_dropdown_icona_in_modale(self, trigger):
        """Come seleziona_option_casuale_dropdown_icona, ma senza attendere
        la scomparsa dello scrim: usa questa versione quando il dropdown si
        trova dentro una modale (es. 'Tier' nella modale 'Nuova Carta'),
        perché lo scrim della modale resta sempre visibile finché la modale
        è aperta e l'attesa andrebbe in timeout."""
        trigger_locator = self._risolvi_trigger(trigger)

        campo = trigger_locator.locator(
            "xpath=ancestor::div[contains(concat(' ', normalize-space(@class), ' '), ' v-field ')][1]"
        )
        icona = campo.locator(".mdi-menu-down")
        self._scrolla_al_centro(icona)
        icona.click()

        opzioni = self.page.locator(".v-overlay-container [role='option']")
        opzioni.first.wait_for(state="visible")

        count = opzioni.count()
        if count > 0:
            indice_casuale = random.randint(0, count - 1)
            opzioni.nth(indice_casuale).click()

    def salva_html_pagina(self, nome_file: str = "page_source", elemento=None, cartella: str = "debug_html"):
        """Salva su file l'HTML della pagina (o di un elemento specifico) per
        ispezione offline dei selettori, come il 'page source' di Appium.

        Utile quando serve capire velocemente il markup reale generato da
        Vuetify (es. ruoli accessibili, classi, testo concatenato label+valore)
        senza doverlo scoprire a tentativi con errori di strict mode o timeout.

        :param nome_file: nome del file (senza estensione), es. "modale_tier"
        :param elemento: stringa CSS o Locator dell'elemento di cui salvare
                        l'HTML. Se None, salva l'intera pagina.
        :param cartella: cartella locale dove salvare il file
                        (creata automaticamente se non esiste)
        :return: percorso completo del file salvato
        """
        import os
        from datetime import datetime

        os.makedirs(cartella, exist_ok=True)

        if elemento is not None:
            elemento_locator = self._risolvi_trigger(elemento)
            html = elemento_locator.evaluate("el => el.outerHTML")
        else:
            html = self.page.content()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        percorso_file = os.path.join(cartella, f"{nome_file}_{timestamp}.txt")

        with open(percorso_file, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"HTML salvato in: {percorso_file}")
        return percorso_file

            # --- DIAGNOSTICA HTML SU FILE (stile 'page_source' Appium) ---
        # Salva l'HTML della pagina (o di un elemento specifico) su un file .txt
        # locale, cosi puoi aprirlo nell'editor e cercare selettori (role=,
        # aria-label=, class=) senza dover indovinare a colpi di test falliti.
        #
        # Esempi d'uso:
        #   fidelity.salva_html_pagina("dump_completo")
        #       -> salva tutta la pagina, utile quando non sai ancora
        #          dove guardare
        #
        #   fidelity.salva_html_pagina("modale_nuova_carta",
        #                              elemento=fidelity.page.get_by_role("dialog"))
        #       -> salva solo la modale, molto piu' leggibile e mirato
        #
        #   campagne.salva_html_pagina("riga_condizione",
        #                              elemento=campagne._righe_campo_condizione().last)
        #       -> salva solo un componente specifico, utile per capire
        #          il testo/markup reale di una singola riga dinamica
        #          (es. il pattern "Totale Carrello\nCampo" scoperto su Tier/Campo)
        #
        # I file finiscono in debug_html/ con timestamp nel nome, cosi non
        # si sovrascrivono tra un run e l'altro. Usalo PRIMA di scrivere un
        # nuovo locator per un componente Vuetify sconosciuto, invece di
        # scoprirlo via TimeoutError/strict mode violation nei test.

    def compila_orario(self, trigger, orario: str):
        """Compila un campo <input type="time"> Vuetify (stringa CSS o Locator).

        :param trigger: selettore CSS o Locator del campo orario
        :param orario: orario nel formato "HH:MM" (formato richiesto dagli
                       input HTML type="time", es. "09:30")
        """
        trigger_locator = self._risolvi_trigger(trigger)
        trigger_locator.fill(orario)

    def seleziona_prima_opzione_dropdown_icona_in_modale(self, trigger):
        """Come seleziona_prima_opzione_dropdown_icona, ma senza attendere
        la scomparsa dello scrim: usa questa versione quando il dropdown si
        trova dentro una modale (es. 'Template' nella modale 'Nuova
        Schedulazione'), perché lo scrim della modale resta sempre visibile
        finché la modale è aperta e l'attesa andrebbe in timeout."""
        trigger_locator = self._risolvi_trigger(trigger)

        campo = trigger_locator.locator(
            "xpath=ancestor::div[contains(concat(' ', normalize-space(@class), ' '), ' v-field ')][1]"
        )
        icona = campo.locator(".mdi-menu-down")
        self._scrolla_al_centro(icona)
        icona.click()

        opzioni = self.page.locator(".v-overlay-container [role='option']")
        opzioni.first.wait_for(state="visible")
        opzioni.first.click()

    def seleziona_option_casuale_dropdown_no_force_new(self, trigger_locator=None):
        if trigger_locator:
            trigger_locator.click()

        # Cerca le opzioni nell'overlay (supporta sia [role='button'] che [role='option'])
        opzioni = self.page.locator(".v-overlay-container [role='button'], .v-overlay-container [role='option']")
        
        # Attendi che almeno un'opzione sia visibile
        opzioni.first.wait_for(state="visible", timeout=10000)
        
        count = opzioni.count()
        if count > 0:
            index_casuale = random.randint(0, count - 1)
            opzioni.nth(index_casuale).click()

        # --- GESTIONE DIALOG NATIVI DEL BROWSER (window.confirm/alert) ---

    def gestisci_prossimo_dialog(self, accetta: bool = True):
        """Registra un listener one-shot per il prossimo dialog nativo del
        browser (window.confirm/alert/prompt), es. 'Eliminare questa
        registrazione di spreco?'.

        IMPORTANTE: va chiamato PRIMA del click che genera il dialog
        (page.once si registra in anticipo), perché il dialog nativo blocca
        l'esecuzione JS della pagina finché non viene gestito — se il
        listener non è già registrato quando il dialog appare, il test
        va in timeout.

        :param accetta: True per cliccare "Ok", False per "Annulla"
        """
        if accetta:
            self.page.once("dialog", lambda dialog: dialog.accept())
        else:
            self.page.once("dialog", lambda dialog: dialog.dismiss())


    def seleziona_suggerimento_casuale_dropdown_in_modale(self, trigger):
        """
        Gestisce il click su dropdown di tipo Autocomplete/Suggerimenti in modale 
        (es. Mapping Articoli) dove le voci mostrate non sono opzioni standard role='option'.
        """
        trigger_locator = self._risolvi_trigger(trigger)

        # Identifica il campo Vuetify ed espande la dropdown tramite l'icona o il focus
        campo = trigger_locator.locator(
            "xpath=ancestor::div[contains(concat(' ', normalize-space(@class), ' '), ' v-field ')][1]"
        )
        icona = campo.locator(".mdi-menu-down")
        
        if icona.count() > 0 and icona.is_visible():
            self._scrolla_al_centro(icona)
            icona.click()
        else:
            trigger_locator.click()

        # Cerca tutti i possibili elementi cliccabili nell'overlay (sia v-list-item che ruoli generici)
        overlay = self.page.locator(".v-overlay-container")
        suggerimenti = overlay.locator(".v-list-item, [role='option'], [role='button']")
        
        # Attende che la lista di suggerimenti sia visibile
        suggerimenti.first.wait_for(state="visible", timeout=10000)

        count = suggerimenti.count()
        if count > 0:
            indice_casuale = random.randint(0, count - 1)
            suggerimento = suggerimenti.nth(indice_casuale)
            
            # Scrolla ed esegue il click sull'elemento scelto
            self._scrolla_al_centro(suggerimento)
            suggerimento.click()

            # Verifica che l'overlay sia scomparso; in caso contrario preme Escape per chiuderlo forzatamente
            try:
                overlay.locator(".v-overlay__content").wait_for(state="hidden", timeout=2000)
            except Exception:
                self.page.keyboard.press("Escape")

    


   