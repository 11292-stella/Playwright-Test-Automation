from playwright.sync_api import Page, expect
from pages.base_page import BasePage
import re
import random


class Campagne(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # --- NUOVA CAMPAGNA ---
        self.btn_nuova_campagna = page.get_by_role("button", name="Nuova Campagna")

        # --- COMPILA MODULO GENERALE ---
        self.input_nome_campagna = page.get_by_role("textbox", name="Nome Campagna")
        self.input_descrizione = page.get_by_role("textbox", name="Descrizione")
        self.input_priorita = page.get_by_role("spinbutton", name="Priorita")
        self.campo_tipo = (
            page.get_by_role("dialog")
            .locator(".v-select")
            .filter(has_text=re.compile(r"Tipo"))
            .locator(".v-field__input")
        )

        # --- TAB CONDIZIONI ---
        self.tab_condizioni = page.get_by_role("tab", name="Condizioni")
        self.btn_condizione = page.get_by_role("button", name="Condizione", exact=True)
        self.btn_gruppo = page.get_by_role("button", name="Gruppo", exact=True)
        self.btn_and = page.get_by_role("button", name="AND", exact=True)
        self.btn_or = page.get_by_role("button", name="OR", exact=True)

        # --- TAB AZIONI ---
        self.tab_azioni = page.get_by_role("tab", name="Azioni")
        self.btn_aggiungi_azione = page.get_by_role("button", name="Aggiungi Azione")

               # --- TAB PROGRAMMAZIONE ---
        self.tab_programmazione = page.get_by_role("tab", name="Programmazione")
        self.input_data_inizio = page.get_by_role("textbox", name="Data Inizio")
        self.input_data_fine = page.get_by_role("textbox", name="Data Fine")
        self.testo_fasce_orarie = page.get_by_text("Fasce Orarie", exact=True)
        self.btn_aggiungi_fascia = page.get_by_role("button", name="Aggiungi Fascia")

                # --- TAB TARGETING ---
        self.tab_targeting = page.get_by_role("tab", name="Targeting")
        self.input_max_utilizzi_totali = page.get_by_role("spinbutton", name="Max Utilizzi Totali")
        self.input_max_utilizzi_cliente = page.get_by_role("spinbutton", name="Max Utilizzi per Cliente")
        self.input_importo_minimo_carrello = page.get_by_role("spinbutton", name="Importo Minimo Carrello")
        self.input_sconto_massimo = page.get_by_role("spinbutton", name="Sconto Massimo (cap)")
        # --- SALVATAGGIO ---
        self.btn_salva = page.get_by_role("button", name="Salva")

    # --- NAVIGAZIONE ---

    def apri_campagne_fidelity(self):
        self.apri_gruppo_menu("Fidelity")
        self.naviga_a("/fidelity/campaigns")

    # --- NUOVA CAMPAGNA / TAB GENERALE ---

    def crea_nuova_campagna(self):
        self.btn_nuova_campagna.click()

    def compila_generale(self, dati_mod):
        self.input_nome_campagna.fill(dati_mod["nome"])
        self.input_descrizione.fill(dati_mod["descrizione"])
        self.input_priorita.fill(str(dati_mod["priorita"]))

    def seleziona_tipo_casuale(self):
        self.seleziona_option_casuale_dropdown_icona_in_modale(self.campo_tipo)

    # --- TAB CONDIZIONI: NAVIGAZIONE ---

    def naviga_a_tab_condizioni(self):
        self.tab_condizioni.click()

    # --- TAB CONDIZIONI: GESTIONE RIGHE/GRUPPI ---

    def aggiungi_condizione(self):
        """Clicca l'ultimo bottone 'Condizione' visibile: se sei nel gruppo
        root aggiunge lì, se hai appena aperto/selezionato un sottogruppo
        aggiunge nel sottogruppo (il bottone 'Condizione' più vicino/ultimo
        nel DOM corrisponde al gruppo attivo più recente)."""
        self.btn_condizione.last.click()

    def aggiungi_gruppo(self):
        self.btn_gruppo.last.click()

    def imposta_operatore_logico(self, indice_gruppo: int = 0, operatore: str = "AND"):
        """indice_gruppo: 0 = gruppo root, 1 = primo sottogruppo, ecc.
        operatore: 'AND' oppure 'OR'."""
        self.page.get_by_role("button", name=operatore, exact=True).nth(indice_gruppo).click()

    # --- TAB CONDIZIONI: COMPILAZIONE RIGA ---
    #
    # NOTA: ogni campo 'Campo'/'Operatore' arriva già precompilato con un
    # valore di default (es. testo reale = "Totale Carrello\nCampo", non
    # "Campo" da solo), quindi il filtro deve cercare la label alla FINE
    # del testo (has_text con regex "Campo$"), non un match esatto.
    # Scoping esplicito al dialog per escludere i filtri "Tipo"/"Stato"
    # della pagina lista campagne sullo sfondo.

    def _righe_campo_condizione(self):
        return (
            self.page.get_by_role("dialog")
            .locator(".v-select")
            .filter(has_text=re.compile(r"Campo$"))
        )

    def _righe_operatore_condizione(self):
        return (
            self.page.get_by_role("dialog")
            .locator(".v-select")
            .filter(has_text=re.compile(r"Operatore$"))
        )

    def compila_ultima_condizione(self, valore_testo: str = "Categoria A", valore_numero: str = "10"):
        """Seleziona Campo e Operatore in modo casuale sull'ultima riga
        condizione aggiunta (l'ultima nel DOM) e riempie il Valore con un
        valore coerente al tipo di campo effettivamente presente.

        Il Campo e' scelto casualmente, quindi non si puo' sapere in anticipo
        se il Valore risultante sara' un textbox o uno spinbutton: il metodo
        rileva il tipo e sceglie valore_testo o valore_numero di conseguenza.
        """
        self.seleziona_option_casuale_dropdown_icona_in_modale(
            self._righe_campo_condizione().last.locator(".v-field__input")
        )
        self.seleziona_option_casuale_dropdown_icona_in_modale(
            self._righe_operatore_condizione().last.locator(".v-field__input")
        )

        dialog = self.page.get_by_role("dialog")
        spinbutton = dialog.get_by_role("spinbutton", name="Valore")
        if spinbutton.count() > 0:
            spinbutton.last.fill(valore_numero)
        else:
            dialog.get_by_role("textbox", name="Valore").last.fill(valore_testo)

    # --- TAB AZIONI: NAVIGAZIONE ---

    def naviga_a_tab_azioni(self):
        self.tab_azioni.click()

    # --- TAB AZIONI: GESTIONE RIGHE ---

    def aggiungi_azione(self):
        self.btn_aggiungi_azione.click()

    def _righe_tipo_azione(self):
        """Come per 'Campo'/'Operatore' in Condizioni: il testo reale
        contiene il valore di default gia' selezionato prima della label
        (es. 'Sconto Percentuale\nTipo Azione'), quindi si filtra sulla
        fine del testo, non su un match esatto."""
        return (
            self.page.get_by_role("dialog")
            .locator(".v-select")
            .filter(has_text=re.compile(r"Tipo Azione$"))
        )

    # Tipi Azione i cui campi extra sono stati verificati via dump HTML
    # e sono gestiti da compila_ultima_azione. Il modulo ha 11 Tipi Azione
    # totali (percentDiscount, fixedDiscount, fixedPrice, nthItemDiscount,
    # buyXgetYfree, singleItemMultibuy, buyXplusSaveYpercent,
    # pointsMultiplier, bonusPoints, cashbackPercent, freeItem): ognuno
    # mostra campi diversi (es. 'Compra X Ricevi Y Gratis' mostra 'Compra X
    # (gruppo)'/'Y gratis'/'Categorie target'/'Prodotti target', non
    # gestiti qui). Espandi questa lista solo dopo aver verificato con
    # salva_html_pagina() i campi reali di un nuovo tipo.
    TIPI_AZIONE_GESTITI = ["Prodotto Gratis", "Punti Bonus"]

    def seleziona_tipo_azione(self, testo_tipo: str):
        self.seleziona_option_per_testo_dropdown_in_modale(
            self._righe_tipo_azione().last.locator(".v-field__input"),
            testo_tipo,
        )

    def seleziona_tipo_azione_casuale_sicuro(self):
        """Sceglie un Tipo Azione a caso, ma SOLO tra quelli in
        TIPI_AZIONE_GESTITI, cosi' compila_ultima_azione trova sempre
        i campi che si aspetta di compilare."""
        tipo = random.choice(self.TIPI_AZIONE_GESTITI)
        self.seleziona_tipo_azione(tipo)

    # --- TAB AZIONI: COMPILAZIONE RIGA ---

    def compila_ultima_azione(self, quantita: str = "2", valore_testo: str = "10", nome_etichetta: str = ""):
        """Seleziona un Tipo Azione casuale sull'ultimo blocco azione
        aggiunto, poi compila SOLO i campi che compaiono di conseguenza:
        il Tipo Azione scelto determina quali campi extra appaiono
        (es. 'Prodotto Gratis' mostra Prodotto omaggio/Quantita/Nome
        etichetta, 'Punti Bonus' mostra solo Valore). Ogni campo viene
        controllato con .count() prima di essere compilato, esattamente
        come gia' fatto per il Valore delle Condizioni.

        NOTA: seleziona solo tra i Tipi Azione in TIPI_AZIONE_GESTITI,
        gli unici i cui campi extra sono stati verificati e sono coperti
        dalla logica qui sotto. Se in futuro aggiungi altri tipi alla
        whitelist, verifica prima con salva_html_pagina() quali campi
        mostrano e aggiungi il ramo corrispondente.
        """
        self.seleziona_tipo_azione_casuale_sicuro()

        dialog = self.page.get_by_role("dialog")

        prodotto_omaggio = dialog.get_by_role("combobox", name="Prodotto omaggio")
        if prodotto_omaggio.count() > 0:
            prodotto_omaggio.last.click()
            opzioni = self.page.locator(".v-overlay-container [role='option']")
            opzioni.first.wait_for(state="visible")
            count = opzioni.count()
            if count > 0:
                opzioni.nth(random.randint(0, count - 1)).click()

        quantita_field = dialog.get_by_role("spinbutton", name="Quantità")
        if quantita_field.count() > 0:
            quantita_field.last.fill(quantita)

        if nome_etichetta:
            nome_field = dialog.get_by_role("textbox", name="Nome (etichetta)")
            if nome_field.count() > 0:
                nome_field.last.fill(nome_etichetta)

        valore_spin = dialog.get_by_role("spinbutton", name="Valore")
        valore_text = dialog.get_by_role("textbox", name="Valore")
        if valore_spin.count() > 0:
            valore_spin.last.fill(valore_testo)
        elif valore_text.count() > 0:
            valore_text.last.fill(valore_testo)

    # --- TAB PROGRAMMAZIONE: NAVIGAZIONE ---

    def naviga_a_tab_programmazione(self):
        self.tab_programmazione.click()

    def compila_date_validita(self, dati_mod):
        """Compila Data Inizio/Data Fine del tab Programmazione con
        compila_data() di BasePage (input type="date", formato YYYY-MM-DD
        indipendentemente dal display gg/mm/aaaa).

        :param dati_mod: dict con chiavi "attiva_dal" e "fino_al",
                         tipicamente ChainTestData.genera_dati_campagna()
        """
        self.compila_data(self.input_data_inizio, dati_mod["attiva_dal"])
        self.compila_data(self.input_data_fine, dati_mod["fino_al"])

    # --- TAB PROGRAMMAZIONE: GIORNI DELLA SETTIMANA ---
    #
    # NOTA: i giorni (Dom/Lun/Mar/Mer/Gio/Ven/Sab) non hanno un ruolo
    # accessibile stabile. Il codegen ha registrato due strategie diverse
    # sullo stesso form (get_by_text esatto per alcuni, span+regex "^Ven$"
    # per altri), quindi qui proviamo prima get_by_text e usiamo lo span
    # come fallback se non e' presente/cliccabile. Sembra un toggle:
    # click ripetuti sullo stesso giorno lo attivano/disattivano (visto
    # nel codegen su "Mar" cliccato due volte di fila).

    def _giorno_locator(self, nome_giorno: str):
        testo = self.page.get_by_text(nome_giorno, exact=True)
        if testo.count() > 0:
            return testo.first
        return self.page.locator("span").filter(has_text=re.compile(rf"^{nome_giorno}$")).first

    def toggle_giorno(self, nome_giorno: str):
        """Seleziona/deseleziona un singolo giorno (es. 'Lun'). Chiamarlo
        due volte sullo stesso giorno annulla la selezione."""
        self._giorno_locator(nome_giorno).click()

    def seleziona_giorni(self, giorni: list):
        """Seleziona una lista di giorni, es. ['Dom', 'Lun', 'Gio', 'Ven']."""
        for giorno in giorni:
            self.toggle_giorno(giorno)

    def seleziona_giorni_casuali(self, n: int = 3):
        """Seleziona n giorni casuali tra i 7 disponibili."""
        tutti_i_giorni = ["Dom", "Lun", "Mar", "Mer", "Gio", "Ven", "Sab"]
        giorni_scelti = random.sample(tutti_i_giorni, k=min(n, len(tutti_i_giorni)))
        self.seleziona_giorni(giorni_scelti)

    # --- TAB PROGRAMMAZIONE: FASCE ORARIE ---

    def espandi_fasce_orarie(self):
        self.testo_fasce_orarie.click()

    def aggiungi_fascia_oraria(self):
        self.btn_aggiungi_fascia.click()

    def compila_ultima_fascia_oraria(self, dati_fascia):
        """Compila i campi orario (Dalle/Alle) dell'ultima fascia oraria
        aggiunta, usando compila_orario() di BasePage (per input type="time",
        formato HH:MM) invece di compila_data() (pensato per input
        type="date", formato YYYY-MM-DD).

        NOTA: le label "Dalle"/"Alle" sono un'ipotesi ancora da confermare
        con salva_html_pagina() sulla riga fascia appena aggiunta, esattamente
        come fatto per i Tipi Azione con TIPI_AZIONE_GESTITI. Aggiorna i
        get_by_label qui sotto una volta verificato il markup reale.

        :param dati_fascia: dict con chiavi "ora_inizio" e "ora_fine"
                            (formato "HH:MM"), tipicamente generato da
                            ChainTestData.genera_dati_fascia_oraria()
        """
        dialog = self.page.get_by_role("dialog")
        self.compila_orario(dialog.get_by_label("Dalle").last, dati_fascia["ora_inizio"])
        self.compila_orario(dialog.get_by_label("Alle").last, dati_fascia["ora_fine"])

    def compila_programmazione(self, giorni: list = None, dati_fasce: list = None):
        """Compila l'intero tab Programmazione: seleziona i giorni indicati
        (o 3 casuali se non specificati), espande 'Fasce Orarie' e aggiunge
        una riga per ogni dizionario in dati_fasce, compilandola subito con
        compila_ultima_fascia_oraria().

        Se dati_fasce e' None, aggiunge una sola fascia vuota (utile finche'
        le label reali dei campi Dalle/Alle non sono state confermate col
        dump HTML).

        :param giorni: lista di giorni es. ['Dom', 'Lun', 'Gio', 'Ven']
        :param dati_fasce: lista di dict [{"ora_inizio": "09:00", "ora_fine": "12:00"}, ...],
                           tipicamente da ChainTestData.genera_dati_fascia_oraria()
        """
        self.seleziona_giorni(giorni) if giorni else self.seleziona_giorni_casuali()

        self.espandi_fasce_orarie()

        if dati_fasce:
            for dati_fascia in dati_fasce:
                self.aggiungi_fascia_oraria()
                self.compila_ultima_fascia_oraria(dati_fascia)
        else:
            self.aggiungi_fascia_oraria()

                # --- TAB TARGETING: NAVIGAZIONE ---

    def naviga_a_tab_targeting(self):
        self.tab_targeting.click()

    # --- TAB TARGETING: CHIP TIER/CANALI ---
    #
    # NOTA: stesso comportamento dei giorni in Programmazione. Il codegen
    # ha usato get_by_text(exact=True) per "standard"/"pos"/"kiosk"/"web",
    # ma per "app" ha dovuto usare span+regex "^app$" (probabile match
    # parziale con altro testo in pagina, es. "webapp"). Riuso lo stesso
    # helper con fallback usato per _giorno_locator.

    TIER_DISPONIBILI = ["standard", "silver", "gold", "platinum"]
    CANALI_DISPONIBILI = ["pos", "kiosk", "app", "web"]

    def _chip_locator(self, testo: str):
        testo_locator = self.page.get_by_text(testo, exact=True)
        if testo_locator.count() > 0:
            return testo_locator.first
        return self.page.locator("span").filter(has_text=re.compile(rf"^{testo}$")).first

    def toggle_tier(self, nome_tier: str):
        """Seleziona/deseleziona un Tier (es. 'gold'). Toggle: chiamarlo
        due volte sullo stesso tier annulla la selezione."""
        self._chip_locator(nome_tier).click()

    def seleziona_tier(self, tier: list):
        for nome_tier in tier:
            self.toggle_tier(nome_tier)

    def seleziona_tutti_i_tier(self):
        self.seleziona_tier(self.TIER_DISPONIBILI)

    def toggle_canale(self, nome_canale: str):
        """Seleziona/deseleziona un Canale (es. 'app'). Toggle: chiamarlo
        due volte sullo stesso canale annulla la selezione."""
        self._chip_locator(nome_canale).click()

    def seleziona_canali(self, canali: list):
        for nome_canale in canali:
            self.toggle_canale(nome_canale)

    def seleziona_tutti_i_canali(self):
        self.seleziona_canali(self.CANALI_DISPONIBILI)

    # --- TAB TARGETING: LIMITI DI UTILIZZO ---

    def compila_limiti_utilizzo(self, dati_targeting):
        """Compila i 4 campi numerici del tab Targeting. Il codegen li ha
        solo cliccati (focus, senza digitare), quindi qui restano ai valori
        di default (-1 / EUR 0 = nessun limite) a meno che dati_targeting
        non fornisca un valore. Ogni chiave e' opzionale: se assente il
        campo viene lasciato invariato.

        :param dati_targeting: dict con chiavi opzionali "max_utilizzi_totali",
                               "max_utilizzi_cliente", "importo_minimo_carrello",
                               "sconto_massimo"
        """
        if "max_utilizzi_totali" in dati_targeting:
            self.input_max_utilizzi_totali.fill(str(dati_targeting["max_utilizzi_totali"]))
        if "max_utilizzi_cliente" in dati_targeting:
            self.input_max_utilizzi_cliente.fill(str(dati_targeting["max_utilizzi_cliente"]))
        if "importo_minimo_carrello" in dati_targeting:
            self.input_importo_minimo_carrello.fill(str(dati_targeting["importo_minimo_carrello"]))
        if "sconto_massimo" in dati_targeting:
            self.input_sconto_massimo.fill(str(dati_targeting["sconto_massimo"]))

    def compila_targeting(self, dati_targeting=None):
        """Compila l'intero tab Targeting: seleziona tutti i Tier e tutti
        i Canali (come mostrato nello screenshot, dove risultano tutti
        gia' evidenziati), poi compila i limiti numerici se forniti."""
        self.seleziona_tutti_i_tier()
        self.seleziona_tutti_i_canali()
        if dati_targeting:
            self.compila_limiti_utilizzo(dati_targeting)


    # --- SALVATAGGIO ---

    def salva_campagna(self):
        """Clicca 'Salva' e attende la risposta della chiamata di salvataggio,
        cosi' il chiamante puo' controllare status_code/body invece di
        affidarsi solo alla scomparsa del loader."""
        return self.clicca_e_attendi_risposta(
            self.btn_salva,
            re.compile(r"/fidelity/campaig"),
        )