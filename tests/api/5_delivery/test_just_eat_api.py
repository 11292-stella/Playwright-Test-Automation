import pytest
from playwright.sync_api import APIRequestContext
from support.api_helpers import assert_status, assert_field, assert_unauthorized


class TestJustEatApi:
    """Suite di test diretti alle API di integrazione e menu Just Eat."""

    def test_get_just_eat_integration(self, api_context: APIRequestContext):
        """Verifica il recupero della configurazione dell'integrazione Just Eat."""
        response = api_context.get("/v1/delivery-integrations/justeat")
        assert_status(response, 200)
        data = response.json()
        assert data is not None

    def test_update_just_eat_integration(self, api_context: APIRequestContext):
        """Testa l'aggiornamento delle impostazioni Just Eat via PUT."""
        payload = {
            "enabled": False,
            "brandId": "",
            "siteIds": [],
            "settings": {
                "autoAccept": False,
                "defaultPrepMinutes": 10,
                "markupPercent": 11,
                "coverImageUrl": "https://picsum.photos/1920/1080"
            }
        }
        response = api_context.put("/v1/delivery-integrations/justeat", data=payload)
        assert_status(response, 200)

    def test_get_just_eat_menu_status(self, api_context: APIRequestContext):
        """Verifica lo stato del menu Just Eat."""
        response = api_context.get("/v1/delivery-menu/justeat/status")
        assert_status(response, 200)

    def test_get_categories_just_eat(self, api_context: APIRequestContext):
        """Verifica il recupero del catalogo categorie per il canale Just Eat."""
        response = api_context.get("/api/webapp-catalog/categories?channel=justeat")
        assert_status(response, 200)

    def test_just_eat_unauthorized(self, api_context_no_auth: APIRequestContext):
        """Verifica che le chiamate senza autenticazione restituiscano 401."""
        assert_unauthorized(api_context_no_auth, "get", "/v1/delivery-integrations/justeat")

    def test_lifecycle_categoria_just_eat_api(self, api_context: APIRequestContext):
        """Testa il ciclo di vita completo (POST, PUT, DELETE) di una categoria Just Eat via API."""
        # 1. Creazione nuova categoria
        create_payload = {
            "label": "Bevande UNISCI API JustEat",
            "description": "Descrizione da test API JustEat",
            "imageUrl": "",
            "mediaId": "media_mqgk80gl_2ed36dd82f8d65cb",
            "displayOrder": 10,
            "sourceCategoryId": "test-cat-justeat-001",
            "channel": "justeat"
        }
        create_res = api_context.post("/api/webapp-catalog/categories", data=create_payload)
        assert_status(create_res, 200)

        body = create_res.json()
        assert_field(body, "channel", "justeat")
        cat_id = body.get("id") or body.get("_id")
        assert cat_id, "ID categoria assente nella risposta della POST"

        try:
            # 2. Recupero prodotti disponibili per la categoria creata
            avail_res = api_context.get(f"/api/webapp-catalog/categories/{cat_id}/available-products?channel=justeat")
            assert_status(avail_res, 200)

            # 3. Svuotamento/Associazione prodotti alla categoria
            update_prod_payload = {
                "productIds": [],
                "channel": "justeat"
            }
            update_res = api_context.put(f"/api/webapp-catalog/categories/{cat_id}/products", data=update_prod_payload)
            assert_status(update_res, 200)

        finally:
            # 4. Cleanup: eliminazione categoria creata
            delete_res = api_context.delete(f"/api/webapp-catalog/categories/{cat_id}")
            assert_status(delete_res, 200)

    # per avviare test: pytest tests/5_delivery/test_just_eat_api.py -s
    # per avviare script: $env:API_DISCOVERY=1; pytest tests/5_delivery/test_just_eat.py --headed -s