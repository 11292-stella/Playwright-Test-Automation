import pytest
from playwright.sync_api import APIRequestContext
from support.api_helpers import assert_status, assert_field, assert_unauthorized


class TestGlovoApi:
    """Suite di test diretti alle API di integrazione e menu Glovo."""

    def test_get_glovo_integration(self, api_context: APIRequestContext):
        response = api_context.get("/v1/delivery-integrations/glovo")
        assert_status(response, 200)
        data = response.json()
        assert data is not None

    def test_glovo_unauthorized(self, api_context_no_auth: APIRequestContext):
        """Verifica che senza autenticazione risponda 401."""
        assert_unauthorized(api_context_no_auth, "get", "/v1/delivery-integrations/glovo")

    def test_lifecycle_categoria_glovo_api(self, api_context: APIRequestContext):
        # 1. Creazione nuova categoria
        create_payload = {
            "label": "Bevande UNISCI API",
            "description": "Descrizione da test API",
            "imageUrl": "",
            "mediaId": "media_mqgk80gl_2ed36dd82f8d65cb",
            "displayOrder": 0,
            "sourceCategoryId": "test-cat-api-001",
            "channel": "glovo"
        }
        create_res = api_context.post("/api/webapp-catalog/categories", data=create_payload)
        assert_status(create_res, 200)
        
        body = create_res.json()
        assert_field(body, "channel", "glovo")
        cat_id = body.get("id") or body.get("_id")

        try:
            # 2. Verifica recupero prodotti disponibili
            avail_res = api_context.get(f"/api/webapp-catalog/categories/{cat_id}/available-products?channel=glovo")
            assert_status(avail_res, 200)

            # 3. Aggiornamento prodotti
            update_res = api_context.put(
                f"/api/webapp-catalog/categories/{cat_id}/products", 
                data={"productIds": [], "channel": "glovo"}
            )
            assert_status(update_res, 200)

        finally:
            # 4. Cleanup
            delete_res = api_context.delete(f"/api/webapp-catalog/categories/{cat_id}")
            assert_status(delete_res, 200)

            # per eseguire script: $env:API_DISCOVERY=1; pytest tests/5_delivery/test_glovo.py --headed -s
            # per eseguire test: pytest tests/5_delivery/test_glovo.py --headed -s