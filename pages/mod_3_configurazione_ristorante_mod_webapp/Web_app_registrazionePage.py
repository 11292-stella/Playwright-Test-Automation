import random
from playwright.sync_api import Page
from pages.base_page import BasePage


class WebAppRegistrazione(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # --- APRI TAB PRINCIPALE ---
        self.apri_tab_app_registrazione = page.get_by_role("tab", name="Webapp Registrazione Clienti")

        # --- SOTTOTAB ---
        self.tab_branding = page.get_by_role("tab", name="Branding", exact=True)
        self.tab_testi = page.get_by_role("tab", name="Testi", exact=True)
        self.tab_immagini = page.get_by_role("tab", name="Immagini", exact=True)
        self.tab_verifica = page.get_by_role("tab", name="Verifica", exact=True)
        self.tab_campi_form = page.get_by_role("tab", name="Campi Form", exact=True)
        self.tab_privacy = page.get_by_role("tab", name="Privacy", exact=True)
        self.tab_hand_off = page.get_by_role("tab", name="Hand-off",exact=True)
        self.tab_stampa_qr = page.get_by_role("tab", name="Stampa QR",exact=True)

        # --- BRANDING: TEMA (stesso pattern già usato per App Asporto) ---
        self.tema_classico = page.get_by_text("Classico", exact=True)
        self.tema_elegante = page.get_by_text("Elegante", exact=True)
        self.tema_moderno = page.get_by_text("Moderno", exact=True)
        self.tema_scuro = page.get_by_text("Scuro", exact=True)
        self.temi_disponibili = [self.tema_classico, self.tema_elegante, self.tema_moderno, self.tema_scuro]

        # --- TESTI ---
        self.input_tagline = page.get_by_role("textbox", name="Tagline")
        self.input_messaggio_benvenuto = page.get_by_role("textbox", name="Messaggio di benvenuto")
        self.input_titolo_form = page.get_by_role("textbox", name="Titolo form")
        self.input_titolo_successo = page.get_by_role("textbox", name="Titolo schermata di successo")
        self.input_messaggio_successo = page.get_by_role("textbox", name="Messaggio di successo")
        self.input_consenso_marketing = page.get_by_role("textbox", name="Testo consenso marketing")
        self.input_footer = page.get_by_role("textbox", name="Footer")
        self.input_note_legali = page.get_by_role("textbox", name="Note legali")

        # --- IMMAGINI ---
        self.btn_seleziona_immagine = page.get_by_role("button", name="Seleziona")
        self.immagine_placeholder = page.locator(".v-responsive__content")
        self.btn_conferma_immagine = page.get_by_role("button", name="Conferma")

        # --- VERIFICA ---
        self.testi_opzioni_verifica = [
            "Solo email (magic link)",
            "Solo telefono (OTP SMS)",
            "Entrambi (email + SMS)",
            "Nessuna (sconsigliato)",
        ]
        self.dropdown_metodo_verifica = self.dropdown_per_testo("Modalità")

        # --- PRIVACY ---
        self.btn_inserisci_mod = page.get_by_role("button", name="Inserisci modello base")

        # --- HAND_OFF ---
        self.switch_qr = page.get_by_role("checkbox", name="Mostra QR temporaneo")

        # --- STAMPA QR ---
        self.testo_invio = page.get_by_role("textbox", name="Testo invito")
        self.dropdown_formato_stampa = self.dropdown_per_testo("Formato stampa")
        self.btn_scarica_pdf = page.get_by_role("button", name="Scarica PDF")
        


        # --- CAMPI FORM ---
    CAMPI_CON_OBBLIGATORIO = ["Data di nascita", "Indirizzo completo", "Lingua preferita", "Allergie / note"]
    CAMPI_SOLO_VISIBILE = ["Consenso marketing email", "Consenso marketing SMS", "Consenso profilazione"]


    # --- NAVIGAZIONE ---
    def apri_app_registrazione(self):
        self.apri_gruppo_menu("Gestione Locale")
        self.naviga_a("/restaurant-config")
        self.apri_tab_app_registrazione.click()

    def vai_a_branding(self):
        self.tab_branding.click()

    def vai_a_testi(self):
        self.tab_testi.click()

    def vai_a_immagini(self):
        self.tab_immagini.click()

    def vai_a_verifica(self):
        self.tab_verifica.click()

    def vai_a_campi_form(self):
        self.tab_campi_form.click()

    def vai_a_privacy(self):
        self.tab_privacy.click()

    def vai_a_hand_off(self):
        self.tab_hand_off.click()

    def vai_a_stampa_qr(self):
        self.tab_stampa_qr.click()

    # --- BRANDING ---
    def seleziona_tema_random(self):
        random.choice(self.temi_disponibili).click()

    # --- TESTI ---
    def compila_testi(self, dati_testi: dict):
        self.input_tagline.fill(dati_testi["tagline"])
        self.input_messaggio_benvenuto.fill(dati_testi["messaggio_benvenuto"])
        self.input_titolo_form.fill(dati_testi["titolo_form"])
        self.input_titolo_successo.fill(dati_testi["titolo_successo"])
        self.input_messaggio_successo.fill(dati_testi["messaggio_successo"])
        self.input_consenso_marketing.fill(dati_testi["consenso_marketing"])
        self.input_footer.fill(dati_testi["footer"])
        self.input_note_legali.fill(dati_testi["note_legali"])

    # --- IMMAGINI ---
    def seleziona_tutte_le_immagini(self):
        """Seleziona un'immagine per ogni campo immagine del tab. Dopo ogni
        selezione il bottone 'Seleziona' del campo cambia stato, quindi il
        conteggio residuo si riduce ad ogni giro (ecco perché nel record
        c'erano 3 click con .first e l'ultimo senza)."""
        while self.btn_seleziona_immagine.count() > 0:
            self.btn_seleziona_immagine.first.click()
            self.immagine_placeholder.click()
            self.btn_conferma_immagine.click()

    # --- VERIFICA ---
    def seleziona_metodo_verifica_random(self):
        self.seleziona_option_casuale_dropdown_no_force(self.dropdown_metodo_verifica)

    # --- CAMPI FORM ---

    def _switch_riga_campo_form(self, nome_campo: str):
        """Individua i 2 switch (Visibile, Obbligatorio, in quest'ordine) della
        riga del campo dato nel tab 'Campi Form'. Localizzati tramite il testo
        della label invece dell'id dello switch, perché gli id generati da
        Vuetify (es. #switch-v-330) sono dinamici e cambiano ad ogni render.
 
        :return: tupla (switch_visibile, switch_obbligatorio)
        """
        riga = self.page.get_by_text(nome_campo, exact=True).locator("xpath=ancestor::tr[1]")
        switches = riga.locator("input[type='checkbox']")
        return switches.nth(0), switches.nth(1)

    def configura_campi_form_random(self):
        """Attiva in modo casuale 3 o 4 campi opzionali del form (diversi ad
        ogni esecuzione), rendendoli Visibili. Per i campi che supportano
        anche Obbligatorio, decide anch'esso in modo casuale, rispettando la
        dipendenza: Obbligatorio va attivato SOLO dopo aver attivato Visibile."""
        tutti_i_campi = self.CAMPI_CON_OBBLIGATORIO + self.CAMPI_SOLO_VISIBILE
        campi_scelti = random.sample(tutti_i_campi, random.choice([3, 4]))
 
        for nome_campo in campi_scelti:
            switch_visibile, switch_obbligatorio = self._switch_riga_campo_form(nome_campo)
 
            switch_visibile.check()
 
            if nome_campo in self.CAMPI_CON_OBBLIGATORIO and random.choice([True, False]):
                switch_obbligatorio.check()


    # --- PRIVACY ---
    def usa_mod_base(self):
        self.btn_inserisci_mod.click()

    # --- HAND OFF ---
    def mostra_qr(self):
        self.switch_qr.click()

    # --- STAMPA QR ---
    def stampa_qr(self, dati_qr:dict):
        self.testo_invio.fill(dati_qr["testo"])

    def seleziona_formato_stampa_random(self):
     self.seleziona_option_casuale_dropdown_no_force(self.dropdown_formato_stampa)

    def scarica_pdf(self):
        """Clicca 'Scarica PDF' e salva il file in locale (cartella 'downloads'),
        senza aprire il dialog nativo di salvataggio del sistema operativo.
        :return: percorso completo del PDF scaricato
        """
        return self.clicca_e_scarica(self.btn_scarica_pdf)