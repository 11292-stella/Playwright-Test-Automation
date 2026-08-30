from playwright.sync_api import Page, expect
from pages.base_page import BasePage

class Catalogo(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # --- ELEMENTI CATALOGO PAGE
        self.catalogo_catena = page.get_by_label("Catena")
        self.click_su_attiva = page.get_by_role("button", name="Attiva modifica catalogo")
        self.modifica_prodotti = page.get_by_role("main").get_by_text("Prodotti", exact=True)
        self.nuovo_prodotto = page.get_by_role("button", name="Nuovo Prodotto")

        # --- ELEMENTI MODALE NUOVO PRODOTTO ---
        self.campo_sku = page.get_by_role("textbox", name="SKU", exact=True)
        self.nome_prodotto = page.get_by_role("textbox", name="Nome Prodotto *")
        self.descrizione = page.get_by_role("textbox", name="Descrizione", exact=True)
        self.dropdown_tipo_prodotto = page.get_by_label("Tipo Prodotto")
        self.prezzo_vendita = page.get_by_label("Prezzo Vendita")
        self.costo_vendita = page.get_by_label("Costo")
        self.dropdown_misura = page.get_by_label("Unità di Misura")
        self.crea_prodotto = page.get_by_role("button", name="Crea Prodotto")

        # --- ESCI DA MODIFICA CATENA ---
        self.esci_da_modifica_catena = page.get_by_role("button", name="Esci da modifica catena")

        # --- ELEMENTI CATEGORIE ---
        self.modifica_categorie = page.get_by_role("main").get_by_text("Categorie", exact=True)

        # --- CREA NUOVA CATEGORIA ---
        self.click_nuova_categoria = page.get_by_role("button", name="Nuova Categoria")

        # --- ELEMENTI NUOVA CATEGORIA ---
        self.nome_categoria_nuova = page.get_by_role("textbox", name="Nome *")
        self.descrizione_categoria_nuova = page.get_by_role("textbox", name="Descrizione", exact=True)
        self.crea_categoria = page.get_by_role("button", name="Crea")

        # --- CREA NUOVO INGREDIENTE ---
        self.click_nuovo_ingrediente = page.get_by_role("main").get_by_text("Ingredienti", exact=True)
        

        # --- ELEMENTI NUOVO INGREDIENTE ---
        self.apri_modale_ingrediente = page.get_by_role("button", name="Nuovo Ingrediente").first
        self.campo_sku_ingrediente = page.get_by_role("textbox", name="SKU / Codice *")
        self.nome_ingrediente_nuovo = page.get_by_role("textbox", name="Nome *")
        self.descrizione_ingrediente = page.get_by_role("textbox", name="Descrizione")
        self.costo_standard =page.get_by_role("spinbutton", name="Costo Standard")
        self.costo_unitario = page.get_by_role("spinbutton", name="Costo Unitario (WACO)")
        self.densita = page.get_by_role("spinbutton", name="Densita (kg/l)")
        self.dropdown_iva = page.get_by_label("IVA acquisto")
        self.crea_ingrediente = page.get_by_role("button", name="Crea")

        # --- CREA NUOVA VARIANTE ---
        self.click_nuova_variante = page.get_by_role("main").get_by_text("Varianti", exact=True)

        # --- ELEMENTI NUOVA VARIANTE ---
        self.apri_modale_variante = page.get_by_role("button", name="Nuova Variante").first
        self.nome_variante = page.get_by_role("textbox", name="Nome *")
        self.descrizione_variante = page.get_by_role("textbox", name="Descrizione")
        self.delta_quantita = page.get_by_role("spinbutton", name="Delta Quantità", description="Quantità sottratta dal magazzino (valore positivo)")
        self.crea_fine_variante = page.get_by_role("button", name="Crea Variante")

        # --- CREA NUOVO LISTINO ---
        self.click_nuovo_listino = page.get_by_role("main").get_by_text("Listini", exact=True) 
        self.apri_modale_listino = page.get_by_role("button", name="Nuovo Listino").first
        self.codice_listino = page.get_by_role("textbox", name="Codice")
        self.nome_listino = page.get_by_role("textbox", name="Nome")
        self.descrizione_listino = page.get_by_role("textbox", name="Descrizione") 
        self.data_dal = page.get_by_role("textbox", name="Valido dal")
        self.data_al = page.get_by_role("textbox", name="Valido fino al")
        self.crea_listino_finale = page.get_by_role("button", name="Crea")

        # CLICK PROPAGA A TUTTI I NEGOZI ---
        self.click_propaga = page.get_by_role("button", name="Propaga a tutti i negozi")



        # --- NAVIGAZIONE ---
    def apri_catalogo(self):
            """Naviga fino a Clienti Catena (Gestione catene > Catalogo Catena)."""
            self.apri_gruppo_menu("Gestione catene")
            self.naviga_a("/chain-catalog")

        # --- AZIONI ---
    def filtra_per_catena(self, nome_catena: str):
         """Seleziona una catena specifica dal filtro."""
         self.seleziona_option_per_testo_dropdown(self.catalogo_catena, nome_catena)
         self.attendi_scomparsa_loader()

    def click_attiva(self):
         self.click_su_attiva.click()

    def modifica_e_crea_prodotti(self):
         self.modifica_prodotti.click()

    def crea_nuovo_prodotto(self):
         expect(self.nuovo_prodotto).to_be_visible(timeout=15000)
         self.nuovo_prodotto.click()

    def compila_nuovo_prodotto(self, dati_prodotto: dict):
         """Compila la modale 'Nuovo Prodotto' con i dati passati (vedi ChainTestData.genera_dati_nuovo_prodotto_catalogo_catena).
         Per ora compila solo lo SKU: aggiungeremo gli altri campi uno alla volta."""
         self.campo_sku.fill(dati_prodotto["sku"])
         self.nome_prodotto.fill(dati_prodotto["nome_prodotto"])
         self.descrizione.fill(dati_prodotto["descrizione"])
         


    def seleziona_prezzi_e_costi(self, dati_prodotto: dict):
         self.prezzo_vendita.fill(str(dati_prodotto["prezzo_vendita"]))
         self.costo_vendita.fill(str(dati_prodotto["costo"]))

    def seleziona_unita_di_misura_prodotto(self):
         """Seleziona un'opzione casuale dal dropdown 'Unità di Misura' nel modale 'Nuovo Prodotto'.

         NOTA: stessa modale/stesso motivo di seleziona_tipo_prodotto, vedi
         il commento lì per il perché NON usiamo la variante _no_force."""
         self._scrolla_al_centro(self.dropdown_misura)
         self.seleziona_option_casuale_dropdown(self.dropdown_misura)

    def crea_prodotto_catalogo(self):
         self.crea_prodotto.click()

    def esci_da_modifica(self):
         self.esci_da_modifica_catena.click()

    def modifica_e_crea_categorie(self):
         self.modifica_categorie.click()

    def creazione_nuova_categoria(self):
         self.click_nuova_categoria.click()

    def compila_nuova_categoria(self, dati_categoria: dict):
         """Compila la modale 'Nuova Categoria' con i dati passati
         (vedi ChainTestData.genera_dati_nuova_categoria_catena)."""
         self.nome_categoria_nuova.fill(dati_categoria["nome_categoria"])
         self.descrizione_categoria_nuova.fill(dati_categoria["descrizione"])
         self.crea_categoria.click()

    def creazione_nuovo_ingrediente(self):
         self.click_nuovo_ingrediente.click()

    def apertura_e_compilazione_nuovo_ingrediente(self):
         self.apri_modale_ingrediente.click()

    def compila_nuovo_ingrediente(self, dati_ingrediente: dict):
         self.campo_sku_ingrediente.fill(dati_ingrediente["sku_ingrediente"])
         self.nome_ingrediente_nuovo.fill(dati_ingrediente["nome_prodotto"])
         self.descrizione_ingrediente.fill(dati_ingrediente["descrizione_ingrediente"])
         self.costo_standard.fill(str(dati_ingrediente["costo_standard"]))
         self.costo_unitario.fill(str(dati_ingrediente["costo_unitario"]))
         self.densita.fill(str(dati_ingrediente["densita"]))

    def seleziona_iva_acquisto(self):
         """Seleziona un'opzione casuale dal dropdown 'IVA acquisto'."""
         self.seleziona_option_casuale_dropdown(self.dropdown_iva)
         self.crea_ingrediente.click()

    def modifica_e_crea_varianti(self):
         self.click_nuova_variante.click()

    def apri_nuova_variante(self):
         self.apri_modale_variante.click()

    def compila_nuova_variante(self,dati_variante: dict):
         self.nome_variante.fill(dati_variante["nome_variante"])
         self.descrizione_variante.fill(dati_variante["descrizione_variante"])
         self.delta_quantita.fill(str(dati_variante["delta_quantita"]))
         self.crea_fine_variante.click()

    def modifica_e_crea_nuovo_listino(self):
         self.click_nuovo_listino.click()

    def apri_nuovo_listino(self):
         self.apri_modale_listino.click()

    def compila_nuovo_listino(self, dati_listino: dict):
         self.codice_listino.fill(dati_listino["codice_listino"])
         self.nome_listino.fill(dati_listino["nome_listino"])
         self.descrizione_listino.fill(dati_listino["descrizione_listino"])

    def compila_data_listino(self, dati_listino: dict):
          self.compila_data(self.data_dal, dati_listino["data_dal"])
          self.compila_data(self.data_al, dati_listino["data_al"])
          self.crea_listino_finale.click()

    def click_propaga_negozi(self):
         self.click_propaga.click()
          
         

         
         





          
         
     
         
         
    
