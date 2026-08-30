from playwright.sync_api import Page, expect
from pages.base_page import BasePage
import re
import random

class FoodCost(BasePage):
    def __init__(self, page:Page):
        super().__init__(page)

        # --- FILTRI ---
        
        self.btn_genera_dati = page.get_by_role("button", name="Genera Dati")
        self.btn_aggiorna = page.get_by_role("button", name="Aggiorna")

        # --- VISUALIZZA PRODOTTO ---
        self.input_visualizza = page.get_by_role("button").filter(has_text=re.compile(r"^$")).nth(4)

# ============================================================
# NAVIGAZIONE
# ============================================================

    def apri_food_cost(self):
        self.apri_gruppo_menu("Controllo Gestione")
        self.naviga_a("/cost-control/food-cost")

# ============================================================
# SELEZIONA FILTRI
# ============================================================
    def seleziona_da_drop(self):
        """
        Apre il menu periodo (v-menu, non v-select) cliccando sul bottone
        che mostra il periodo corrente, poi seleziona un'opzione casuale
        dall'overlay che si apre.
        """
        opzioni_periodo = ["Ultimo Mese", "Ultimo Anno", "Ultimo Trimestre", "Ultima Settimana"]
        scelta = random.choice(opzioni_periodo)

        # Il trigger è un bottone (aria-haspopup="menu"), non un .v-field
        trigger = self.page.get_by_role(
            "button",
            name=re.compile(r"Ultimo Mese|Ultimo Anno|Ultimo Trimestre|Ultima Settimana")
        )
        trigger.click()

        overlay = self.page.locator(".v-overlay-container")
        overlay.wait_for(state="visible")

        # Cerca l'opzione SOLO dentro l'overlay (evita ambiguità con il trigger stesso)
        overlay.get_by_text(scelta, exact=True).click()

        self.attendi_scomparsa_loader()

# ============================================================
# GENERA E AGGIORNA
# ============================================================
    def genera_dati_e_aggiorna(self):
        """
        Clicca 'Genera Dati' per popolare/rigenerare i dati di test per il
        periodo selezionato, attende la scomparsa del loader, poi clicca
        'Aggiorna' per ricaricare la vista con i dati appena generati.
        """
        self.btn_genera_dati.click()
        self.attendi_scomparsa_loader()

        self.btn_aggiorna.click()
        self.attendi_scomparsa_loader()

# ============================================================
# VISUALIZZA
# ============================================================
    def visualizza(self):
        """
        Clicca l'icona 'occhio' su una riga della tabella 'Dettaglio
        Analisi Costi' per aprire il dettaglio del prodotto (modale).
        """
        self.input_visualizza.click()
       