import pytest
from support.api_helpers import assert_status, assert_unauthorized, assert_field


# Categoria sorgente nota, stessa categoria di test usata in Gestione
# Categorie/Catalogo Catena (non ricreata qui, riusata come dato fisso).
CATEGORIA_SORGENTE_TEST = "test-cat-001"


@pytest.fixture
def categoria_webapp_asporto_di_test(api_context, faker):
    """
    Crea una categoria del catalogo webapp (channel=asporto) unita a
    partire da una categoria sorgente nota, con label univoca per il
    test corrente invece di riusare una categoria creata a mano.
    """
    payload = {
        "label": faker.unique.word(),
        "description": "categoria webapp asporto di test (creata da pytest)",
        "imageUrl": "",
        "mediaId": None,
        "displayOrder": 50,
        "sourceCategoryId": CATEGORIA_SORGENTE_TEST,
        "channel": "asporto",
    }
    response = api_context.post("/api/webapp-catalog/categories", data=payload)
    assert_status(response, 200)
    return response.json()


class TestWebAppAsportoCatalogoAPI:
    """
    Test API per il modulo Webapp Asporto - Catalogo (mod_3_configurazione_ristorante_mod_webapp).
    Endpoint: GET /api/webapp-catalog/categories, GET /api/app-menus,
    POST /api/webapp-catalog/categories,
    GET .../products, GET .../available-products,
    PUT .../products (assegna prodotti a una categoria webapp),
    POST /api/app-menus.
    Individuati con support/discover_endpoints.py creando una categoria
    webapp e assegnandole dei prodotti.
    NOTA: gli endpoint "copy-from-table" e "copy-from-channel" (con
    overwrite=true) non sono coperti qui: sovrascrivono il catalogo
    webapp condiviso e non sono ripetibili in automazione, stesso motivo
    per cui l'import reale da negozio (mod_1) non è automatizzato.
    """

    def test_lista_categorie_webapp_asporto_status_200(self, api_context):
        response = api_context.get("/api/webapp-catalog/categories", params={"channel": "asporto"})
        assert_status(response, 200)

    def test_lista_menu_app_asporto_status_200(self, api_context):
        response = api_context.get("/api/app-menus", params={"channel": "asporto"})
        assert_status(response, 200)

    def test_crea_categoria_webapp_asporto_status_200(self, categoria_webapp_asporto_di_test):
        assert_field(categoria_webapp_asporto_di_test, "channel", "asporto")

    def test_prodotti_categoria_webapp_asporto_status_200(self, api_context, categoria_webapp_asporto_di_test):
        # NOTA: assumiamo che il body di risposta della POST categoria
        # esponga l'id creato nel campo "id" (visto nel log come
        # ObjectId Mongo, es. "000000000000000000000002"). Se il campo
        # nel body si chiama diversamente, aggiornare qui.
        categoria_id = categoria_webapp_asporto_di_test["id"]
        response = api_context.get(f"/api/webapp-catalog/categories/{categoria_id}/products")
        assert_status(response, 200)

    def test_prodotti_disponibili_categoria_webapp_asporto_status_200(self, api_context, categoria_webapp_asporto_di_test):
        categoria_id = categoria_webapp_asporto_di_test["id"]
        response = api_context.get(f"/api/webapp-catalog/categories/{categoria_id}/available-products")
        assert_status(response, 200)

    def test_assegna_prodotti_categoria_webapp_asporto_status_200(self, api_context, categoria_webapp_asporto_di_test):
        """
        Assegna una lista vuota di prodotti alla categoria appena creata:
        verifica che l'endpoint funzioni senza dover riusare l'enorme
        lista di ID prodotto reali vista nel log manuale.
        """
        categoria_id = categoria_webapp_asporto_di_test["id"]
        response = api_context.put(
            f"/api/webapp-catalog/categories/{categoria_id}/products",
            data={"productIds": [], "channel": "asporto"},
        )
        assert_status(response, 200)

    def test_crea_menu_app_asporto_status_200(self, api_context, faker):
        nome = faker.unique.word()
        payload = {
            "name": {"it": nome, "en": nome},
            "description": {"it": "", "en": ""},
            "imageUrl": "",
            "price": 0,
            "rules": [],
            "availability": {
                "shifts": [],
                "daysOfWeek": [1, 2, 3, 4, 5, 6, 7],
                "startDate": "2026-09-04",
                "endDate": "2026-09-05",
            },
            "active": True,
            "order": 0,
            "channel": "asporto",
        }
        response = api_context.post("/api/app-menus", data=payload)
        assert_status(response, 200)
        assert_field(response.json(), "channel", "asporto")

    def test_lista_categorie_webapp_asporto_senza_auth_401(self, api_context_no_auth):
        assert_unauthorized(
            api_context_no_auth, "get", "/api/webapp-catalog/categories", params={"channel": "asporto"}
        )

    def test_crea_categoria_webapp_asporto_senza_auth_401(self, api_context_no_auth):
        payload = {
            "label": "No Auth",
            "description": "",
            "imageUrl": "",
            "mediaId": None,
            "displayOrder": 0,
            "sourceCategoryId": CATEGORIA_SORGENTE_TEST,
            "channel": "asporto",
        }
        assert_unauthorized(api_context_no_auth, "post", "/api/webapp-catalog/categories", data=payload)

        # per eseguire: pytest tests/api/3_configurazione_ristorante_mod_webapp/test_web_app_asporto_catalogo_api.py -v
        # per eseguire script per endpoint: python -m support.discover_endpoints