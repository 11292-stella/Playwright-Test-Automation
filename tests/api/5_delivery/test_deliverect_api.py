import pytest
from support.api_helpers import assert_status, assert_unauthorized, assert_field


@pytest.fixture
def categoria_deliverect(api_context, faker):
    """
    Crea una categoria specifica per il canale "deliverect", con
    dati dinamici (faker) per garantire l'isolamento dei test.
    """
    payload = {
        "label": f"Cat Deliverect {faker.unique.word()}",
        "description": "Categoria di test Deliverect (creata da pytest API)",
        "imageUrl": "",
        "mediaId": "",
        "displayOrder": 1,
        "sourceCategoryId": "test-cat-deliverect-001",
        "channel": "deliverect",
    }
    response = api_context.post("/api/webapp-catalog/categories", data=payload)
    assert_status(response, 200)
    data = response.json()
    
    yield data
    
    # Cleanup: elimina la categoria creata se l'id è presente
    cat_id = _extract_id(data)
    if cat_id:
        api_context.delete(f"/api/webapp-catalog/categories/{cat_id}")


def _extract_id(categoria: dict) -> str:
    """Estragga l'ID della categoria provando le chiavi più comuni."""
    for candidate in ("id", "_id", "categoryId", "webappCategoryId"):
        if candidate in categoria:
            return categoria[candidate]
    raise KeyError(
        f"Nessuna chiave id nota trovata in categoria_deliverect. "
        f"Chiavi disponibili: {list(categoria.keys())}"
    )


class TestDeliverectAPI:
    """
    Test API per il modulo Delivery > Deliverect (mod_5_delivery).
    Endpoint individuati tramite API discovery dal test E2E:
      - GET    /v1/delivery-integrations/deliverect
      - GET    /v1/delivery-menu/deliverect/status
      - GET    /api/webapp-catalog/categories?channel=deliverect
      - POST   /api/webapp-catalog/categories
      - GET    /api/webapp-catalog/categories/{id}/products
      - GET    /api/webapp-catalog/categories/{id}/available-products
      - PUT    /api/webapp-catalog/categories/{id}/products
      - DELETE /api/webapp-catalog/categories/{id}
    """

    def test_stato_integrazione_deliverect_status_200(self, api_context):
        """Verifica il recupero della configurazione dell'integrazione Deliverect."""
        response = api_context.get("/v1/delivery-integrations/deliverect")
        assert_status(response, 200)

    def test_stato_menu_deliverect_status_200(self, api_context):
        """Verifica lo stato di sincronizzazione del menu Deliverect."""
        response = api_context.get("/v1/delivery-menu/deliverect/status")
        assert_status(response, 200)

    def test_lista_categorie_deliverect_status_200(self, api_context):
        """Verifica l'ottenimento delle categorie filtrate per canale deliverect."""
        response = api_context.get(
            "/api/webapp-catalog/categories", params={"channel": "deliverect"}
        )
        assert_status(response, 200)

    def test_crea_categoria_deliverect_status_200(self, categoria_deliverect):
        """Verifica che la creazione della categoria restituisca la label corretta."""
        assert_field(categoria_deliverect, "label")

    def test_prodotti_categoria_deliverect_status_200(self, api_context, categoria_deliverect):
        """Verifica la lista prodotti associati alla categoria Deliverect."""
        cat_id = _extract_id(categoria_deliverect)
        response = api_context.get(f"/api/webapp-catalog/categories/{cat_id}/products")
        assert_status(response, 200)

    def test_prodotti_disponibili_deliverect_status_200(self, api_context, categoria_deliverect):
        """Verifica i prodotti disponibili da poter associare alla categoria."""
        cat_id = _extract_id(categoria_deliverect)
        response = api_context.get(
            f"/api/webapp-catalog/categories/{cat_id}/available-products",
            params={"channel": "deliverect"},
        )
        assert_status(response, 200)

    def test_aggiorna_prodotti_categoria_deliverect_status_200(self, api_context, categoria_deliverect):
        """Verifica l'assegnazione di una lista vuota di prodotti alla categoria."""
        cat_id = _extract_id(categoria_deliverect)
        payload = {"productIds": [], "channel": "deliverect"}
        response = api_context.put(
            f"/api/webapp-catalog/categories/{cat_id}/products", data=payload
        )
        assert_status(response, 200)

    def test_elimina_categoria_deliverect_status_200(self, api_context, faker):
        """Verifica l'eliminazione esplicita via DELETE di una categoria."""
        payload = {
            "label": f"Cat Temp {faker.unique.word()}",
            "channel": "deliverect",
        }
        create_res = api_context.post("/api/webapp-catalog/categories", data=payload)
        assert_status(create_res, 200)
        cat_id = _extract_id(create_res.json())

        delete_res = api_context.delete(f"/api/webapp-catalog/categories/{cat_id}")
        assert_status(delete_res, 200)

    def test_integrazione_deliverect_senza_auth_401(self, api_context_no_auth):
        """Verifica la protezione 401 Unauthorized sugli endpoint Deliverect."""
        assert_unauthorized(api_context_no_auth, "get", "/v1/delivery-integrations/deliverect")

    def test_categorie_deliverect_senza_auth_401(self, api_context_no_auth):
        """Verifica la protezione 401 sul catalogo categorie Deliverect."""
        assert_unauthorized(
            api_context_no_auth,
            "get",
            "/api/webapp-catalog/categories",
            params={"channel": "deliverect"},
        )

# per eseguire tets: pytest tests/api/5_delivery/test_deliverect_api.py -v
# per eseguire script: $env:API_DISCOVERY=1; pytest tests/5_delivery/test_deliverect.py --headed -s