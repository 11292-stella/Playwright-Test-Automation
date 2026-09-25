import pytest
from support.api_helpers import assert_status, assert_unauthorized, assert_field


@pytest.fixture
def categoria_webapp_tavolo(api_context, faker):
    """
    Crea una categoria per il canale "tavolo" del catalogo webapp, con
    nome univoco, così i test a valle (products, available-products,
    assegnazione) hanno una categoria propria invece di dipendere da
    quelle create a mano nel browser.
    """
    payload = {
        "label": faker.unique.word(),
        "description": "categoria di test (creata da pytest)",
        "imageUrl": "",
        "mediaId": "",
        "displayOrder": 1,
        "sourceCategoryId": "test-cat-001",
        "channel": "tavolo",
    }
    response = api_context.post("/api/webapp-catalog/categories", data=payload)
    assert_status(response, 200)
    return response.json()


def _extract_id(categoria: dict) -> str:
    """
    Il campo id nella risposta di creazione categoria non si chiama
    "id" (visto in un run reale: 'type', 'label', 'description',
    'imageUrl', ... senza 'id' tra le prime chiavi). Proviamo le
    varianti più comuni; se nessuna esiste, l'errore mostra tutte le
    chiavi reali così scegliamo quella giusta al volo.
    """
    for candidate in ("id", "_id", "categoryId", "webappCategoryId"):
        if candidate in categoria:
            return categoria[candidate]
    raise KeyError(
        f"Nessuna chiave id nota trovata in categoria_webapp_tavolo. "
        f"Chiavi disponibili: {list(categoria.keys())}"
    )


class TestWebAppTavoloCatalogoAPI:
    """
    Test API per il modulo Configurazione Ristorante > Web App Tavolo >
    Catalogo (mod_3_configurazione_ristorante_mod_webapp).
    Endpoint individuati con l'API discovery agganciata al test E2E
    esistente (tests/3_configurazione_ristorante_mod_webapp/test_web_app_tavolo_catalogo.py):
      - GET  /api/webapp-catalog/categories
      - GET  /api/categories
      - GET  /api/app-menus
      - GET  /api/webapp-catalog/categories/{id}/products
      - GET  /api/webapp-catalog/categories/{id}/available-products
      - POST /api/webapp-catalog/categories
      - PUT  /api/webapp-catalog/categories/{id}/products
    """

    def test_lista_categorie_webapp_status_200(self, api_context):
        response = api_context.get("/api/webapp-catalog/categories", params={"channel": "tavolo"})
        assert_status(response, 200)

    def test_lista_categorie_generiche_status_200(self, api_context):
        """Endpoint usato per popolare il selettore "importa categoria da"."""
        response = api_context.get("/api/categories")
        assert_status(response, 200)

    def test_lista_app_menus_status_200(self, api_context):
        response = api_context.get("/api/app-menus", params={"channel": "tavolo"})
        assert_status(response, 200)

    def test_crea_categoria_webapp_status_200(self, categoria_webapp_tavolo):
        assert_field(categoria_webapp_tavolo, "label")

    def test_prodotti_categoria_status_200(self, api_context, categoria_webapp_tavolo):
        categoria_id = _extract_id(categoria_webapp_tavolo)
        response = api_context.get(f"/api/webapp-catalog/categories/{categoria_id}/products")
        assert_status(response, 200)

    def test_prodotti_disponibili_categoria_status_200(self, api_context, categoria_webapp_tavolo):
        categoria_id = _extract_id(categoria_webapp_tavolo)
        response = api_context.get(
            f"/api/webapp-catalog/categories/{categoria_id}/available-products",
            params={"channel": "tavolo"},
        )
        assert_status(response, 200)

    def test_assegna_lista_vuota_prodotti_status_200(self, api_context, categoria_webapp_tavolo):
        """
        Assegna una lista vuota di productIds: verifica il "contratto"
        dell'endpoint (200 + accetta il payload) senza dipendere da ID
        prodotto reali del tenant demo, che cambiano nel tempo.
        Per un test con prodotti veri, prendi qualche id dalla risposta
        di available-products (rilancia con -s per vederla) e passala
        qui dentro productIds.
        """
        categoria_id = _extract_id(categoria_webapp_tavolo)
        payload = {"productIds": [], "channel": "tavolo"}
        response = api_context.put(f"/api/webapp-catalog/categories/{categoria_id}/products", data=payload)
        assert_status(response, 200)

    def test_lista_categorie_webapp_senza_auth_401(self, api_context_no_auth):
        assert_unauthorized(
            api_context_no_auth, "get", "/api/webapp-catalog/categories", params={"channel": "tavolo"}
        )

        

        # per eseguire: pytest tests/api/3_configurazione_ristorante_mod_webapp/test_web_app_tavolo_catalogo_api.py -v
        # per avviare il test con script di endpoint: $env:API_DISCOVERY=1 pytest tests/3_configurazione_ristorante_mod_webapp/test_web_app_tavolo_catalogo.py --headed -s