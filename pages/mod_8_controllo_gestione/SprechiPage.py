from playwright.sync_api import Page, expect
from pages.base_page import BasePage

class Sprechi(BasePage):
    def __init__(self, page:Page):
        super().__init__(page)
        
        # --- NUOVO SPRECO ---
        self.btn_registra_spreco = page.get_by_role("button", name="Registra Spreco")

        # --- RICERCA INGREDIENTE ---
        self.campo_ricerca_ingrediente = (
            page.get_by_role("dialog")
            .locator(".v-field.v-field--appended.v-field--center-affix")
            .first
            .locator("input")
        )

        # --- CAMPI DATI SPRECO ---
        self.quantita_spreco = page.get_by_role("spinbutton", name="Quantità")
        self.dropdown_unita = page.get_by_label("Unità")
        self.dropdown_tipo_spreco = page.get_by_label("Tipo Spreco")
        self.dropdown_motivo = page.get_by_label("Motivo")
        self.note_spreco = page.get_by_role("textbox", name="Note")
        self.salva_spreco = page.get_by_role("dialog").get_by_role("button", name="Salva")



# ============================================================
# NAVIGAZIONE
# ============================================================
    def apri_sprechi(self):
        self.apri_gruppo_menu("Controllo Gestione")
        self.naviga_a("/cost-control/waste")

# ============================================================
# NUOVO SPRECO
# ============================================================
    
    def apri_nuovo_spreco(self):
        self.btn_registra_spreco.click()

# ============================================================
# RICERCA E SELEZIONE INGREDIENTE
# ============================================================

    def cerca_e_seleziona_ingrediente(self, nome_ingrediente: str):
        """Identica a Ricetta.cerca_e_seleziona_ingrediente: fill() imposta
        il valore in un solo colpo (un solo evento 'input'), evitando il
        crash da digitazione carattere-per-carattere già noto su questo
        tipo di campo di ricerca."""
        self.campo_ricerca_ingrediente.click()
        self.campo_ricerca_ingrediente.fill(nome_ingrediente)

        opzione = self.page.get_by_text(nome_ingrediente)
        opzione.wait_for(state="visible")
        opzione.click()

# ============================================================
# DROPDOWN CASUALI 
# ============================================================
    def seleziona_unita_casuale(self):
        self.seleziona_option_casuale_dropdown_icona_in_modale(self.dropdown_unita)

    def seleziona_tipo_spreco_casuale(self):
        self.seleziona_option_casuale_dropdown_icona_in_modale(self.dropdown_tipo_spreco)

    def seleziona_motivo_casuale(self):
        self.seleziona_option_casuale_dropdown_icona_in_modale(self.dropdown_motivo)

# ============================================================
# COMPILAZIONE COMPLETA MODALE
# ============================================================

    def compila_modale_spreco(self, nome_ingrediente: str, dati_spreco: dict):
        self.cerca_e_seleziona_ingrediente(nome_ingrediente)
        self.quantita_spreco.fill(str(dati_spreco["quantita"]))
        self.seleziona_unita_casuale()
        self.seleziona_tipo_spreco_casuale()
        self.seleziona_motivo_casuale()
        self.note_spreco.fill(dati_spreco["note"])
        self.salva_spreco.click()

    # ============================================================
# ELIMINAZIONE
# ============================================================

    def elimina_registrazione(self, nome_ingrediente: str):
        """Elimina la registrazione di spreco appena creata, identificata
        dalla riga che contiene il nome dell'ingrediente in 'Registrazioni
        Recenti'. Nella riga ci sono due icone (occhio=dettaglio,
        cestino=elimina): il cestino è l'ultimo bottone della riga.

        Gestisce anche il window.confirm nativo ("Eliminare questa
        registrazione di spreco?") che appare dopo il click.
        """
        riga = self.page.get_by_role("row", name=nome_ingrediente)
        riga.wait_for(state="visible")

        btn_elimina = riga.get_by_role("button").last

        self.gestisci_prossimo_dialog(accetta=True)
        btn_elimina.click()



    
