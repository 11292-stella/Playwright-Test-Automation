import pytest
from support.api_helpers import assert_status, assert_unauthorized, assert_field


def _extract_id(obj: dict, candidates=("id", "_id", "categoryId")) -> str:
    """
    Le categorie del catalogo webapp non usano un nome di campo fisso
    per l'id (vedi anche test_campagne_marketing_api.py). Proviamo le
    varianti più comuni; se nessuna esiste, l'errore mostra tutte le
    chiavi reali della risposta così scegliamo quella giusta al volo.
    """
    for candidate in candidates:
        if candidate in obj:
            return obj[candidate]
    raise KeyError(f"Nessuna chiave id nota trovata. Chiavi disponibili: {list(obj.keys())}")


@pytest.fixture
def categoria_ubereats_di_test(api_context, faker):
    """
    Crea una categoria nel catalogo webapp per il canale ubereats con
    nome univoco, così i test su prodotti disponibili/associati hanno
    una categoria propria invece di dipendere da quelle create a mano
    nel browser.
    """
    payload = {
        "label": f"pytest {faker.unique.word()}",
        "description": faker.sentence(),
        "imageUrl": "",
        "mediaId": None,
        "displayOrder": 0,
        "sourceCategoryId": None,
        "channel": "ubereats",
    }
    response = api_context.post("/api/webapp-catalog/categories", data=payload)
    assert_status(response, 200)
    return response.json()


class TestUberEatsAPI:
    """
    Test API per il modulo Delivery > Uber Eats (mod_5_delivery).
    Endpoint individuati con l'API discovery agganciata al test E2E
    esistente (tests/5_delivery/test_uber_eats.py):
      - GET    /v1/delivery-integrations/ubereats
      - PUT    /v1/delivery-integrations/ubereats
      - GET    /v1/delivery-menu/ubereats/status
      - GET    /api/webapp-catalog/categories?channel=ubereats
      - POST   /api/webapp-catalog/categories
      - GET    /api/webapp-catalog/categories/{id}/available-products
      - GET    /api/webapp-catalog/categories/{id}/products
      - PUT    /api/webapp-catalog/categories/{id}/products
      - DELETE /api/webapp-catalog/categories/{id}
      - GET    /api/categories
      - GET    /v1/media
      - GET    /v1/media/global
    """

    def test_recupera_configurazione_provider_status_200(self, api_context):
        response = api_context.get("/v1/delivery-integrations/ubereats")
        assert_status(response, 200)

    def test_aggiorna_configurazione_provider_status_200(self, api_context, faker):
        payload = {
            "enabled": False,
            "brandId": "",
            "siteIds": [],
            "settings": {
                "autoAccept": False,
                "defaultPrepMinutes": faker.random_int(min=10, max=60),
                "markupPercent": faker.random_int(min=0, max=30),
                "coverImageUrl": faker.image_url(),
            },
        }
        response = api_context.put("/v1/delivery-integrations/ubereats", data=payload)
        assert_status(response, 200)

    def test_stato_menu_status_200(self, api_context):
        response = api_context.get("/v1/delivery-menu/ubereats/status")
        assert_status(response, 200)

    def test_lista_categorie_status_200(self, api_context):
        response = api_context.get(
            "/api/webapp-catalog/categories", params={"channel": "ubereats"}
        )
        assert_status(response, 200)

    def test_lista_categorie_globali_status_200(self, api_context):
        response = api_context.get("/api/categories")
        assert_status(response, 200)

    def test_lista_media_status_200(self, api_context):
        response = api_context.get("/v1/media", params={"page": 1, "pageSize": 24})
        assert_status(response, 200)

    def test_lista_media_globale_status_200(self, api_context):
        response = api_context.get("/v1/media/global", params={"page": 1, "pageSize": 50})
        assert_status(response, 200)

    def test_crea_categoria_status_200(self, categoria_ubereats_di_test):
        assert_field(categoria_ubereats_di_test, "label")

    def test_prodotti_disponibili_categoria_status_200(self, api_context, categoria_ubereats_di_test):
        categoria_id = _extract_id(categoria_ubereats_di_test)
        response = api_context.get(
            f"/api/webapp-catalog/categories/{categoria_id}/available-products",
            params={"channel": "ubereats"},
        )
        assert_status(response, 200)

    def test_prodotti_categoria_status_200(self, api_context, categoria_ubereats_di_test):
        categoria_id = _extract_id(categoria_ubereats_di_test)
        response = api_context.get(f"/api/webapp-catalog/categories/{categoria_id}/products")
        assert_status(response, 200)

    def test_aggiorna_prodotti_categoria_status_200(self, api_context, categoria_ubereats_di_test):
        """
        Aggiorniamo con una lista prodotti vuota invece di hardcodare
        productId reali del tenant demo, che possono cambiare o non
        esistere più: qui interessa solo verificare che l'endpoint
        accetti l'aggiornamento (200), non il contenuto associato.
        """
        categoria_id = _extract_id(categoria_ubereats_di_test)
        response = api_context.put(
            f"/api/webapp-catalog/categories/{categoria_id}/products",
            data={"productIds": [], "channel": "ubereats"},
        )
        assert_status(response, 200)

    def test_elimina_categoria_status_200(self, api_context, faker):
        """
        Creiamo qui una categoria dedicata invece di riusare la
        fixture condivisa, così la cancellazione non intacca gli altri
        test che dipendono da categoria_ubereats_di_test nello stesso run.
        """
        payload = {
            "label": f"pytest delete {faker.unique.word()}",
            "description": faker.sentence(),
            "imageUrl": "",
            "mediaId": None,
            "displayOrder": 0,
            "sourceCategoryId": None,
            "channel": "ubereats",
        }
        create_response = api_context.post("/api/webapp-catalog/categories", data=payload)
        assert_status(create_response, 200)
        categoria_id = _extract_id(create_response.json())

        # Nota: nel log di discovery la DELETE non ha stampato uno
        # status esplicito (probabilmente per timing dei listener).
        # Verificato al primo run: se il backend risponde 204 invece
        # di 200, aggiornare qui.
        response = api_context.delete(f"/api/webapp-catalog/categories/{categoria_id}")
        assert_status(response, 200)

    def test_configurazione_provider_senza_auth_401(self, api_context_no_auth):
        assert_unauthorized(api_context_no_auth, "get", "/v1/delivery-integrations/ubereats")

    def test_lista_categorie_senza_auth_401(self, api_context_no_auth):
        assert_unauthorized(
            api_context_no_auth,
            "get",
            "/api/webapp-catalog/categories",
            params={"channel": "ubereats"},
        )

    def test_crea_categoria_senza_auth_401(self, api_context_no_auth, faker):
        payload = {
            "label": f"pytest {faker.unique.word()}",
            "channel": "ubereats",
        }
        assert_unauthorized(
            api_context_no_auth, "post", "/api/webapp-catalog/categories", data=payload
        )


# per eseguire: pytest tests/api/5_delivery/test_uber_eats_api.py -v
# per eseguire lo script: $env:API_DISCOVERY=1; pytest tests/5_delivery/test_uber_eats.py --headed -s