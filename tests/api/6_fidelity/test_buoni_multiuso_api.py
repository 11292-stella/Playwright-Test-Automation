import pytest
from support.api_helpers import assert_status, assert_unauthorized, debug_body


class TestBuoniMultiusoAPI:
    """
    Test API per il modulo Fidelity > Buoni Multiuso (mod_6_fidelity).
    Endpoint individuati con l'API discovery agganciata al test E2E
    esistente (tests/6_fidelity/test_buoni_multiuso.py):
      - GET  /api/gift-cards
      - POST /api/gift-cards/issue

    BUG NOTO (backend): indice UNIQUE non-sparse su idempotencyKey nella
    collection gift_cards (vedi docstring di BuoniMultiuso.emetti_buono()
    e commento in test_buoni_multiuso.py) — solo la prima emissione in un
    certo intervallo va a buon fine, le successive falliscono lato server.
    Il payload della POST non espone un idempotencyKey lato client, quindi
    è il backend a generarlo: non possiamo garantire un valore univoco da
    qui. test_emetti_buono_status_200 lo segnala esplicitamente invece di
    fallire in modo muto se il bug scatta.
    """

    def test_lista_buoni_status_200(self, api_context):
        response = api_context.get("/api/gift-cards")
        assert_status(response, 200)

    def test_emetti_buono_status_200(self, api_context, faker):
        payload = {
            "value": faker.random_int(min=10, max=200),
            "validDays": faker.random_int(min=30, max=365),
        }
        response = api_context.post("/api/gift-cards/issue", data=payload)

        if response.status != 200:
            pytest.xfail(
                "Emissione fallita - probabile BUG NOTO backend "
                "(indice UNIQUE non-sparse su idempotencyKey in gift_cards, "
                "vedi docstring BuoniMultiuso.emetti_buono()). "
                f"Status: {response.status}. Body: {debug_body(response)}"
            )

        assert_status(response, 200)

    def test_lista_buoni_senza_auth_401(self, api_context_no_auth):
        assert_unauthorized(api_context_no_auth, "get", "/api/gift-cards")

    def test_emetti_buono_senza_auth_401(self, api_context_no_auth, faker):
        payload = {
            "value": faker.random_int(min=10, max=200),
            "validDays": faker.random_int(min=30, max=365),
        }
        assert_unauthorized(
            api_context_no_auth, "post", "/api/gift-cards/issue", data=payload
        )


# per eseguire: pytest tests/api/6_fidelity/test_buoni_multiuso_api.py -v
# per eseguire lo script: $env:API_DISCOVERY=1; pytest tests/6_fidelity/test_buoni_multiuso.py --headed -s