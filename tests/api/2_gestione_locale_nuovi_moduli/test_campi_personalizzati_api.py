import pytest
from support.api_helpers import assert_status, assert_unauthorized, assert_field, debug_body


@pytest.fixture
def campo_personalizzato_di_test(api_context, faker):
    """
    Crea un campo personalizzato (entity=customer) con key/label univoci
    per il test corrente, invece di riusare un campo creato a mano.

    NB: faker (plugin pytest-faker) è deterministico per nodeid del test,
    quindi senza gestione dedicata la stessa chiave verrebbe rigenerata a
    ogni run e il POST fallirebbe con 409 CUSTOM_FIELD_EXISTS dal secondo
    run in poi. discover_endpoints.py non ha mai mostrato una DELETE per
    questo endpoint, quindi invece di inventare un path di cancellazione
    la fixture tratta il 409 come idempotente: se il campo esiste già,
    lo recupera dalla lista e lo riusa (stesso pattern già validato per
    i DDT tabacchi: "reused": true).
    """
    chiave = faker.unique.bothify(text="campo_test_????##").lower()
    payload = {
        "entity": "customer",
        "key": chiave,
        "type": "text",
        "label": chiave,
        "description": "campo personalizzato di test (creato da pytest)",
        "group": None,
        "options": [],
        "required": False,
        "searchable": False,
        "pii": False,
        "defaultValue": None,
        "validation": {},
        "scope": {
            "admin": True,
            "cassa": False,
            "registration": False,
            "portal": False,
            "portal_edit": False,
        },
    }
    response = api_context.post("/api/custom-fields", data=payload)

    if response.status == 409:
        # Campo già esistente da un run precedente (faker deterministico
        # per nodeid + nessuna DELETE disponibile): lo recuperiamo invece
        # di fallire.
        lista = api_context.get(
            "/api/custom-fields", params={"entity": "customer", "includeInactive": "true"}
        )
        assert_status(lista, 200)
        trovato = next((c for c in lista.json() if c.get("key") == chiave), None)
        assert trovato is not None, (
            f"Campo '{chiave}' risulta già esistente (409) ma non trovato "
            f"nella lista campi customer: {debug_body(lista)}"
        )
        return trovato

    assert_status(response, 200)
    return response.json()


class TestCampiPersonalizzatiAPI:
    """
    Test API per il modulo Campi Personalizzati (mod_2_gestione_locale_nuovi_moduli).
    Endpoint individuati con support/discover_endpoints.py.
    """

    def test_lista_tipi_entita_status_200(self, api_context):
        response = api_context.get("/api/custom-fields/entities")
        assert_status(response, 200)

    def test_lista_campi_personalizzati_cliente_status_200(self, api_context):
        response = api_context.get(
            "/api/custom-fields", params={"entity": "customer", "includeInactive": "true"}
        )
        assert_status(response, 200)

    def test_lista_campi_personalizzati_prodotto_status_200(self, api_context):
        # Stesso endpoint del cliente, solo entity=product (simmetria non
        # confermata direttamente nel log per "product" — verificare se
        # fallisce con 400/404).
        response = api_context.get(
            "/api/custom-fields", params={"entity": "product", "includeInactive": "true"}
        )
        assert_status(response, 200)

    def test_anteprima_import_legacy_cliente_status_200(self, api_context):
        response = api_context.post(
            "/api/custom-fields/import-legacy/customer", data={"dryRun": True}
        )
        assert_status(response, 200)

    def test_crea_campo_personalizzato_status_200(self, campo_personalizzato_di_test):
        assert_field(campo_personalizzato_di_test, "key")
        assert_field(campo_personalizzato_di_test, "entity", "customer")

    def test_lista_tipi_entita_senza_auth_401(self, api_context_no_auth):
        assert_unauthorized(api_context_no_auth, "get", "/api/custom-fields/entities")

    def test_lista_campi_personalizzati_senza_auth_401(self, api_context_no_auth):
        assert_unauthorized(
            api_context_no_auth,
            "get",
            "/api/custom-fields",
            params={"entity": "customer", "includeInactive": "true"},
        )

        # per eseguire: pytest tests/api/2_gestione_locale_nuovi_moduli/test_campi_personalizzati_api.py -v
        # per eseguire script per endpoint: python -m support.discover_endpoints