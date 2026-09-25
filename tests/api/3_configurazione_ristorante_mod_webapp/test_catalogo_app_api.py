import pytest
from support.api_helpers import assert_status, assert_unauthorized, assert_field


@pytest.fixture
def menu_app_di_test(api_context, faker):
    """
    Crea un Menù App (channel=tavolo) con nome univoco per il test
    corrente, invece di riusare un menù creato a mano.
    """
    nome = faker.unique.word()
    payload = {
        "name": {"it": nome, "en": nome},
        "description": {"it": "menù di test (creato da pytest)", "en": ""},
        "imageUrl": "",
        "price": 4,
        "rules": [],
        "availability": {
            "shifts": [],
            "daysOfWeek": [1, 3, 4, 6, 7],
            "startDate": "2026-08-31",
            "endDate": "2026-09-03",
        },
        "active": True,
        "order": 0,
        "channel": "tavolo",
    }
    response = api_context.post("/api/app-menus", data=payload)
    assert_status(response, 200)
    return response.json()


class TestCatalogoAppAPI:
    """
    Test API per il modulo Catalogo App (mod_3_configurazione_ristorante_mod_webapp).
    Endpoint: GET /v1/categories, GET /api/app-menus?channel=,
    GET /v1/products/app-catalog?categoryId=, POST /api/app-menus.
    Individuati con support/discover_endpoints.py filtrando per
    categoria e creando un Menù App.
    """

    def test_lista_categorie_status_200(self, api_context):
        response = api_context.get("/v1/categories")
        assert_status(response, 200)

    def test_lista_menu_app_status_200(self, api_context):
        response = api_context.get("/api/app-menus", params={"channel": "tavolo"})
        assert_status(response, 200)

    def test_catalogo_app_per_categoria_status_200(self, api_context):
        response = api_context.get("/v1/products/app-catalog", params={"categoryId": "bevande"})
        assert_status(response, 200)

    def test_crea_menu_app_status_200(self, menu_app_di_test):
        assert_field(menu_app_di_test, "channel", "tavolo")
        assert_field(menu_app_di_test, "price", 4)

    def test_lista_menu_app_senza_auth_401(self, api_context_no_auth):
        assert_unauthorized(api_context_no_auth, "get", "/api/app-menus", params={"channel": "tavolo"})

    def test_crea_menu_app_senza_auth_401(self, api_context_no_auth):
        payload = {
            "name": {"it": "No Auth", "en": "No Auth"},
            "description": {"it": "", "en": ""},
            "imageUrl": "",
            "price": 1,
            "rules": [],
            "availability": {"shifts": [], "daysOfWeek": [1], "startDate": "2026-08-31", "endDate": "2026-09-03"},
            "active": True,
            "order": 0,
            "channel": "tavolo",
        }
        assert_unauthorized(api_context_no_auth, "post", "/api/app-menus", data=payload)

        # per eseguire: pytest tests/api/3_configurazione_ristorante_mod_webapp/test_catalogo_app_api.py -v
        # per eseguire script per endpoint: python -m support.discover_endpoints