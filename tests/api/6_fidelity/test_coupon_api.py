import pytest
from support.api_helpers import assert_status, assert_unauthorized, debug_body


PAYLOAD_BASE = {
    "minOrderAmount": 10.00,
    "validDays": 15,
    "maxUsage": 100,
    "cardCode": "",
}

TIPI_COUPON = [
    pytest.param(
        {"valueType": "FIXED", "value": 5, "freeProductSku": ""},
        id="sconto_fisso",
    ),
    pytest.param(
        {"valueType": "PERCENT", "value": 10, "freeProductSku": ""},
        id="sconto_percentuale",
    ),
    pytest.param(
        {"valueType": "FREE_PRODUCT", "value": 10, "freeProductSku": "SKU-961197"},
        id="prodotto_gratis",
    ),
]


class TestCouponAPI:
    """
    Test API per il modulo Fidelity > Coupon (mod_6_fidelity).
    Endpoint individuati con l'API discovery agganciata al test E2E
    esistente (tests/6_fidelity/test_coupon.py):
      - GET  /api/fidelity/coupons
      - GET  /v1/products/search
      - POST /api/fidelity/coupons/generate

    BUG NOTO (stesso bug documentato in CampagnePage/test_coupon.py):
    la generazione del coupon risponde sempre 404, indipendentemente dal
    valueType (FIXED, PERCENT, FREE_PRODUCT) o dai dati inseriti — è un
    problema lato backend, non del test. Finché non è risolto non
    facciamo assert su status == 200: verifichiamo solo che il
    comportamento anomalo (404) sia coerente, così il test si rompe in
    modo visibile quando l'app verrà corretta (a quel punto va
    ripristinato l'assert di successo, come da nota nell'E2E).
    """

    def test_lista_coupon_status_200(self, api_context):
        response = api_context.get("/api/fidelity/coupons")
        assert_status(response, 200)

    def test_ricerca_prodotti_status_200(self, api_context):
        response = api_context.get(
            "/v1/products/search", params={"q": "Pollo alla Cacciatora", "limit": 50}
        )
        assert_status(response, 200)

    @pytest.mark.parametrize("dati_tipo", TIPI_COUPON)
    def test_genera_coupon_status_404_bug_noto(self, api_context, dati_tipo):
        payload = {**PAYLOAD_BASE, **dati_tipo}
        response = api_context.post("/api/fidelity/coupons/generate", data=payload)

        if response.status == 200:
            pytest.fail(
                "La generazione ora risponde 200: il bug sembra risolto. "
                "Ripristinare l'assert di successo e rimuovere questa "
                "gestione temporanea (compreso il commento in test_coupon.py "
                "lato E2E)."
            )

        assert response.status == 404, (
            f"Status inatteso per il bug noto: {response.status}. "
            f"Body: {debug_body(response)}"
        )

    def test_lista_coupon_senza_auth_401(self, api_context_no_auth):
        assert_unauthorized(api_context_no_auth, "get", "/api/fidelity/coupons")

    def test_genera_coupon_senza_auth_401(self, api_context_no_auth):
        """
        Non possiamo verificare qui il vero comportamento su richiesta non
        autenticata: il bug noto (route non raggiungibile, vedi classe)
        restituisce 404 anche SENZA auth, quindi la risposta non ci dice
        nulla sul controllo di autorizzazione. Il test resta come sentinella
        del bug: quando la route tornerà a rispondere normalmente, questo
        fallirà con un 401 reale (o qualcos'altro), segnalando che va
        ripristinato un vero assert_unauthorized.
        """
        payload = {**PAYLOAD_BASE, "valueType": "FIXED", "value": 5, "freeProductSku": ""}
        response = api_context_no_auth.post("/api/fidelity/coupons/generate", data=payload)

        assert response.status == 404, (
            "Il comportamento senza auth è cambiato rispetto al bug noto "
            f"(atteso 404, ricevuto {response.status}): verificare se il bug "
            "è stato risolto e se serve ripristinare un vero test "
            f"assert_unauthorized. Body: {debug_body(response)}"
        )

# per eseguire: pytest tests/api/6_fidelity/test_coupon_api.py -v
# per eseguire lo script: $env:API_DISCOVERY=1; pytest tests/6_fidelity/test_coupon.py --headed -s