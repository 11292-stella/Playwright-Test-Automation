from playwright.sync_api import expect
from pages.mod_1_gestione_catene.Catalogo_catenaPage import Catalogo
from utils.test_data import ChainTestData

class TestCatalogo:
    def test_catalogo(self, authenticated_page):
        catalogo = Catalogo(authenticated_page)
        catalogo.apri_catalogo()
        catalogo.filtra_per_catena("Catena Demo (reseller_demo_catena_demo)")
        catalogo.click_attiva()

        # --- MODIFICA PRODOTTI ---
        catalogo.modifica_e_crea_prodotti()

        # --- CREA PRODOTTO ---
        catalogo.crea_nuovo_prodotto()
        dati_prodotto = ChainTestData.genera_dati_nuovo_prodotto_catalogo_catena()
        catalogo.compila_nuovo_prodotto(dati_prodotto)
        catalogo.seleziona_prezzi_e_costi(dati_prodotto)
        catalogo.seleziona_unita_di_misura_prodotto()
        catalogo.crea_prodotto_catalogo()
        catalogo.esci_da_modifica()

        # --- CREA CATEGORIE ---
        catalogo.click_attiva()
        catalogo.modifica_e_crea_categorie()
        catalogo.creazione_nuova_categoria()
        dati_categoria = ChainTestData.genera_dati_nuova_categoria_catena()
        catalogo.compila_nuova_categoria(dati_categoria)
        catalogo.esci_da_modifica()

        # --- CREA INGREDIENTI ---
        catalogo.click_attiva()
        catalogo.creazione_nuovo_ingrediente()
        catalogo.apertura_e_compilazione_nuovo_ingrediente()
        dati_ingrediente = ChainTestData.genera_dati_nuovo_ingrediente_catena()
        catalogo.compila_nuovo_ingrediente(dati_ingrediente)
        catalogo.seleziona_iva_acquisto()
        catalogo.esci_da_modifica()

        # --- CREA NUOVE VARIANTI ---
        catalogo.click_attiva()
        catalogo.modifica_e_crea_varianti()
        catalogo.apri_nuova_variante()
        dati_variante = ChainTestData.genera_dati_nuova_variante_catena()
        catalogo.compila_nuova_variante(dati_variante)
        catalogo.esci_da_modifica()

        # --- CREA NUOVO LISTINO --- 
        catalogo.click_attiva()
        catalogo.modifica_e_crea_nuovo_listino()
        catalogo.apri_nuovo_listino()
        dati_listino = ChainTestData.genera_dati_nuovo_listino_catena()
        catalogo.compila_nuovo_listino(dati_listino)
        catalogo.compila_data_listino(dati_listino)
        catalogo.esci_da_modifica()
        catalogo.click_attiva()

        # --- PROPAGA A TUTTI I NEGOZI ---
        catalogo.click_propaga_negozi()
        
        




# per avviare il test: pytest tests/1_gestione_catene/test_catalogo_catena.py --headed