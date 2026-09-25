import pytest
from support.api_helpers import assert_status, assert_unauthorized, assert_field


@pytest.fixture
def specializzazione_di_test(api_context, faker):
    """
    Crea una specializzazione con nome univoco per il test corrente,
    invece di riusare una specializzazione creata a mano.
    """
    payload = {
        "name": faker.unique.word(),
        "description": "specializzazione di test (creata da pytest)",
        "icon": "mdi-account-star",
        "color": None,
        "displayOrder": 0,
    }
    response = api_context.post("/api/staff-specializations", data=payload)
    assert_status(response, 200)
    return response.json()


class TestSpecializzazioniPersonaleAPI:
    """
    Test API per il modulo Specializzazioni Personale (mod_2_gestione_locale_nuovi_moduli).
    Endpoint: GET /api/staff-specializations, GET /api/staff-specializations/presets/list,
    POST /api/staff-specializations.
    Individuati con support/discover_endpoints.py creando una
    specializzazione a mano.
    """

    def test_lista_specializzazioni_status_200(self, api_context):
        response = api_context.get("/api/staff-specializations")
        assert_status(response, 200)

    def test_lista_preset_specializzazioni_status_200(self, api_context):
        response = api_context.get("/api/staff-specializations/presets/list")
        assert_status(response, 200)

    def test_crea_specializzazione_status_200(self, specializzazione_di_test):
        assert_field(specializzazione_di_test, "name")

    def test_lista_specializzazioni_senza_auth_401(self, api_context_no_auth):
        assert_unauthorized(api_context_no_auth, "get", "/api/staff-specializations")

    def test_crea_specializzazione_senza_auth_401(self, api_context_no_auth):
        payload = {
            "name": "No Auth",
            "description": "test",
            "icon": "mdi-account-star",
            "color": None,
            "displayOrder": 0,
        }
        assert_unauthorized(api_context_no_auth, "post", "/api/staff-specializations", data=payload)

        # per eseguire: pytest tests/api/2_gestione_locale_nuovi_moduli/test_specializzazioni_personale_api.py -v
        # per eseguire script per endpoint: python -m support.discover_endpoints