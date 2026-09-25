import pytest
from support.api_helpers import assert_status, assert_unauthorized, debug_body


@pytest.fixture
def payload_campagna_completa(faker):
    """
    Payload di creazione campagna con tutte le sezioni (condizioni con
    gruppo annidato AND/OR, azioni multiple, programmazione, targeting,
    limiti), ricalcato sulla struttura osservata via API discovery sul
    test E2E (tests/6_fidelity/test_campagne.py). Non lo estraiamo dalla
    UI: lo costruiamo qui per poterlo riusare/estendere facilmente nei
    vari test.
    """
    return {
        "name": f"pytest {faker.unique.word()}",
        "description": faker.sentence(),
        "type": "DISCOUNT",
        "active": True,
        "stackable": True,
        "priority": faker.random_int(min=1, max=100),
        "startDate": "2026-09-12",
        "endDate": "2027-01-05",
        "conditions": {
            "type": "group",
            "operator": "AND",
            "conditions": [
                {"type": "atom", "field": "cart.totalQty", "op": "LESS_THAN_EQ", "value": "10"},
                {
                    "type": "group",
                    "operator": "OR",
                    "conditions": [
                        {"type": "atom", "field": "fidelity.points", "op": "GREATER_THAN", "value": "10"}
                    ],
                },
            ],
        },
        "actions": [
            {"type": "percentDiscount", "value": 10, "appliesTo": "cartTotal"},
            {"type": "bonusPoints", "value": 10, "appliesTo": "cartTotal"},
        ],
        "schedule": {
            "daysOfWeek": [0, 1, 4, 5],
            "timeRanges": [{"start": "10:00", "end": "16:30"}],
        },
        "targeting": {
            "tiers": ["standard", "silver", "gold", "platinum"],
            "channels": ["pos", "kiosk", "app", "web"],
        },
        "limits": {
            "maxUsageTotal": "3155",
            "maxUsagePerCustomer": "2",
            "minCartAmount": "7.13",
            "maxDiscount": "37.7",
        },
    }


class TestCampagneFidelityAPI:
    """
    Test API per il modulo Fidelity > Campagne (mod_6_fidelity).
    Endpoint individuati con l'API discovery agganciata al test E2E
    esistente (tests/6_fidelity/test_campagne.py):
      - GET  /api/fidelity/campaigns
      - POST /api/fidelity/campaigns
      - GET  /v1/categories
      - GET  /v1/products

    BUG NOTO (segnalato, vedi commento in test_campagne.py): la POST di
    creazione risponde quasi sempre con errore (500 "Invalid conditions:
    Condition must have a valid operator", o 404), ma il record viene
    comunque persistito lato server. L'ID restituito dal frontend in
    caso di "fallimento" non corrisponde a quello reale: le DELETE su
    quell'ID rispondono 404, lasciando campagne fantasma non
    cancellabili. Finché il bug non è risolto:
      - non facciamo assert su status == 200 nella creazione;
      - non tentiamo cleanup via DELETE con l'ID di risposta (creerebbe
        solo altre chiamate 404 senza rimuovere nulla);
      - il test segnala esplicitamente lo stato anomalo, così si rompe
        in modo visibile quando l'app verrà corretta (a quel punto va
        ripristinato l'assert di successo).
    """

    def test_lista_campagne_status_200(self, api_context):
        response = api_context.get("/api/fidelity/campaigns")
        assert_status(response, 200)

    def test_lista_categorie_status_200(self, api_context):
        response = api_context.get("/v1/categories")
        assert_status(response, 200)

    def test_lista_prodotti_status_200(self, api_context):
        response = api_context.get(
            "/v1/products", params={"pageSize": 500, "search": "", "page": 1}
        )
        assert_status(response, 200)

    def test_crea_campagna_status_200(self, api_context, payload_campagna_completa):
        response = api_context.post("/api/fidelity/campaigns", data=payload_campagna_completa)

        if response.status == 200:
            pytest.fail(
                "Il salvataggio ora risponde 200: il bug sembra risolto. "
                "Ripristinare l'assert di successo e rimuovere questa "
                "gestione temporanea (compreso il commento in "
                "test_campagne.py lato E2E)."
            )

        # Bug ancora presente: verifichiamo solo che il comportamento
        # anomalo sia coerente con quanto documentato, senza tentare
        # cleanup (vedi nota nella docstring della classe).
        assert response.status in (404, 500), (
            f"Status inatteso per il bug noto: {response.status}. "
            f"Body: {debug_body(response)}"
        )

    def test_lista_campagne_senza_auth_401(self, api_context_no_auth):
        assert_unauthorized(api_context_no_auth, "get", "/api/fidelity/campaigns")

    def test_crea_campagna_senza_auth_401(self, api_context_no_auth, payload_campagna_completa):
        assert_unauthorized(
            api_context_no_auth,
            "post",
            "/api/fidelity/campaigns",
            data=payload_campagna_completa,
        )


# per eseguire: pytest tests/api/6_fidelity/test_campagne_api.py -v
# per eseguire lo script: $env:API_DISCOVERY=1; pytest tests/6_fidelity/test_campagne.py --headed -s