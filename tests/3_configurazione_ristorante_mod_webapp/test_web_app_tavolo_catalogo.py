from pages.mod_3_configurazione_ristorante_mod_webapp.Web_App_Tavolo_CatalogoPage import WebAppTavoloCatalogo
from utils.test_data import ChainTestData

class TestWebTavoloCatalogo:
    def test_tavolo_catalogo(self,authenticated_page):
        catalogo = WebAppTavoloCatalogo(authenticated_page)
        catalogo.apri_app_tavolo_catalogo()

        # --- NUOVA CATEGORIA ---
        catalogo.nuova_categoria_mod()
        catalogo.seleziona_categoria_importa("Bevande UNISCI")
        catalogo.seleziona_img()
        dati_categoria = ChainTestData.genera_dati_web_app_tavolo_catalogo()
        catalogo.compila_categoria(dati_categoria)
        catalogo.assegna_prodotti()


# per avviare tutti: pytest tests/3_configurazione_ristorante_mod_webapp/test_web_app_tavolo_catalogo.py --headed