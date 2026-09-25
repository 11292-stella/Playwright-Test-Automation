import os
import pytest
from playwright.sync_api import APIRequestContext
from support.api_helpers import assert_status, assert_field, assert_unauthorized

SITE_ID_TEST = os.getenv("SITE_ID_TEST", "Ristorante Demo (demo_tenant_test)")


class TestDeliverooApi:
    """Suite di test diretti alle API di integrazione e menu Deliveroo."""

    def test_get_deliveroo_status(self, api_context: APIRequestContext):
        """Verifica che lo stato del menu Deliveroo risponda correttamente con status 200."""
        response = api_context.get("/v1/delivery-menu/deliveroo/status")
        assert_status(response, 200)
        data = response.json()
        assert data is not None

    def test_get_deliveroo_integration(self, api_context: APIRequestContext):
        """Verifica il recupero delle configurazioni dell'integrazione Deliveroo."""
        response = api_context.get("/v1/delivery-integrations/deliveroo")
        assert_status(response, 200)

    def test_update_deliveroo_integration(self, api_context: APIRequestContext):
        """Testa la modifica delle impostazioni dell'integrazione Deliveroo tramite PUT."""
        payload = {
            "enabled": False,
            "brandId": "",
            "menuId": "",
            "siteIds": [],
            "settings": {
                "autoAccept": False,
                "defaultPrepMinutes": 28,
                "markupPercent": 0,
                "coverImageUrl": "https://placekittens.com/1920/1080",
                "market": "it",
                "mealtimesFromOpeningHours": True,
                "includeBundles": True,
                "bundleChannel": "asporto",
                "posName": ""
            }
        }
        response = api_context.put("/v1/delivery-integrations/deliveroo", data=payload)
        assert_status(response, 200)

    def test_verifica_connessione_deliveroo_api(self, api_context: APIRequestContext):
        """Testa la chiamata di verifica connessione Deliveroo."""
        payload = {
            "siteIds": [SITE_ID_TEST]
        }
        response = api_context.post("/v1/delivery-integrations/deliveroo/test", data=payload)
        # Se le credenziali o siteId non sono validi lato backend, accetta 200 o 404
        assert response.status in [200, 400, 404], (
            f"Status inatteso: {response.status}. Body: {response.text()}"
        )

    def test_deliveroo_unauthorized(self, api_context_no_auth: APIRequestContext):
        """Verifica che la chiamata senza autenticazione risponda 401."""
        assert_unauthorized(api_context_no_auth, "get", "/v1/delivery-integrations/deliveroo")

    def test_lifecycle_categoria_deliveroo_api(self, api_context: APIRequestContext):
        """Testa il ciclo di vita (POST, PUT, DELETE) di una categoria Deliveroo via API."""
        # 1. Creazione nuova categoria
        create_payload = {
            "label": "Bevande UNISCI Deliveroo API",
            "description": "Descrizione da test API Deliveroo",
            "imageUrl": "",
            "mediaId": "media_mqgk80gl_2ed36dd82f8d65cb",
            "displayOrder": 60,
            "sourceCategoryId": "test-cat-deliveroo-001",
            "channel": "deliveroo"
        }
        create_res = api_context.post("/api/webapp-catalog/categories", data=create_payload)
        assert_status(create_res, 200)

        body = create_res.json()
        assert_field(body, "channel", "deliveroo")
        cat_id = body.get("id") or body.get("_id")

        try:
            # 2. Recupero prodotti disponibili per la categoria
            avail_res = api_context.get(f"/api/webapp-catalog/categories/{cat_id}/available-products?channel=deliveroo")
            assert_status(avail_res, 200)

            # 3. Svuotamento/Aggiornamento prodotti associati
            update_prod_payload = {
                "productIds": [],
                "channel": "deliveroo"
            }
            update_res = api_context.put(f"/api/webapp-catalog/categories/{cat_id}/products", data=update_prod_payload)
            assert_status(update_res, 200)

        finally:
            # 4. Cleanup: eliminazione categoria creata
            delete_res = api_context.delete(f"/api/webapp-catalog/categories/{cat_id}")
            assert_status(delete_res, 200)

        # per eseguire lo script: $env:API_DISCOVERY=1; pytest tests/5_delivery/test_deliveroo.py -s
        # per eseguire il test: pytest tests/5_delivery/test_deliveroo.py --headed -s