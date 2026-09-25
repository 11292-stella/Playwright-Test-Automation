import pytest
from support.api_helpers import assert_status, assert_unauthorized, assert_field


def _extract_id(obj: dict, candidates=("id", "_id", "customerId")) -> str:
    """
    Come per gli altri moduli, il nome del campo id non è fisso a
    seconda dell'endpoint. Proviamo le varianti più comuni; se nessuna
    esiste, l'errore mostra tutte le chiavi reali della risposta.
    """
    for candidate in candidates:
        if candidate in obj:
            return obj[candidate]
    raise KeyError(f"Nessuna chiave id nota trovata. Chiavi disponibili: {list(obj.keys())}")


@pytest.fixture
def cliente_di_test(api_context):
    """
    Recupera un cliente esistente dal tenant demo tramite ricerca,
    da riusare come customerId nella creazione della carta fedeltà,
    invece di hardcodare un id che può non esistere più.
    """
    response = api_context.get("/api/customers/cerca", params={"q": "Becker"})
    assert_status(response, 200)
    body = response.json()
    lista = body if isinstance(body, list) else body.get("items") or body.get("data") or []
    assert lista, f"Nessun cliente trovato per la ricerca di test, risposta: {body}"
    return _extract_id(lista[0])


class TestCarteFidelityAPI:
    """
    Test API per il modulo Fidelity > Carte Fidelity (mod_6_fidelity).
    Endpoint individuati con l'API discovery agganciata al test E2E
    esistente (tests/6_fidelity/test_carte_fidelity.py):
      - GET  /api/fidelity/cards
      - GET  /api/fidelity/cards/stats
      - GET  /api/listini
      - GET  /api/customers/cerca
      - POST /api/fidelity/cards
    """

    def test_lista_carte_status_200(self, api_context):
        response = api_context.get("/api/fidelity/cards", params={"pageSize": 10000})
        assert_status(response, 200)

    def test_statistiche_carte_status_200(self, api_context):
        response = api_context.get("/api/fidelity/cards/stats")
        assert_status(response, 200)

    def test_lista_listini_status_200(self, api_context):
        response = api_context.get("/api/listini")
        assert_status(response, 200)

    def test_ricerca_clienti_status_200(self, api_context):
        response = api_context.get("/api/customers/cerca", params={"q": "Becker"})
        assert_status(response, 200)

    def test_crea_carta_fidelity_status_200(self, api_context, cliente_di_test, faker):
        payload = {
            "barcode": f"BC{faker.random_number(digits=10, fix_len=True)}",
            "customerId": cliente_di_test,
            "balancePoints": faker.random_int(min=0, max=1000),
            "balanceCredit": round(faker.pyfloat(min_value=0, max_value=100, right_digits=2), 2),
            "tierLevel": faker.random_element(elements=("standard", "silver", "gold", "platinum")),
            "tierMultiplier": faker.random_int(min=1, max=50),
            "status": "active",
            "priceListId": None,
        }
        response = api_context.post("/api/fidelity/cards", data=payload)
        assert_status(response, 200)
        assert_field(response.json(), "barcode")

    def test_lista_carte_senza_auth_401(self, api_context_no_auth):
        assert_unauthorized(
            api_context_no_auth, "get", "/api/fidelity/cards", params={"pageSize": 10000}
        )

    def test_crea_carta_fidelity_senza_auth_401(self, api_context_no_auth, faker):
        payload = {
            "barcode": f"BC{faker.random_number(digits=10, fix_len=True)}",
            "customerId": "000000000000000000000000",
            "status": "active",
        }
        assert_unauthorized(
            api_context_no_auth, "post", "/api/fidelity/cards", data=payload
        )


# per eseguire: pytest tests/api/6_fidelity/test_carte_fidelity_api.py -v
# per eseguire lo script: $env:API_DISCOVERY=1; pytest tests/6_fidelity/test_carte_fidelity.py --headed -s