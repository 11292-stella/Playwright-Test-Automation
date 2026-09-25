import pytest
from support.api_helpers import assert_status, assert_unauthorized, assert_field


def _payload_base(faker, **overrides):
    payload = {
        "name": f"pytest {faker.unique.word()}",
        "description": faker.sentence(),
        "requiredPoints": faker.random_int(min=100, max=5000),
        "rewardType": "DISCOUNT",
        "discountType": "FIXED",
        "discountValue": round(faker.pyfloat(min_value=1, max_value=100, right_digits=2), 2),
        "freeProductSku": "",
        "creditAmount": 5,
        "couponSpec": {
            "valueType": "PERCENT",
            "value": 10,
            "minOrderAmount": 0,
            "freeProductSku": "",
            "validDays": 30,
            "maxUsage": 1,
        },
        "stock": faker.random_int(min=-1, max=100),
        "minTierLevel": faker.random_element(elements=("standard", "silver", "gold", "platinum")),
    }
    payload.update(overrides)
    return payload


class TestPremiAPI:
    """
    Test API per il modulo Fidelity > Premi (mod_6_fidelity).
    Endpoint individuati con l'API discovery agganciata al test E2E
    esistente (tests/6_fidelity/test_premi.py):
      - GET  /api/fidelity/rewards
      - GET  /api/fidelity/topup-config
      - PUT  /api/fidelity/topup-config (switch mostra/avvisa in cassa,
        stesso endpoint condiviso con il modulo Impostazioni)
      - GET  /v1/products/search
      - POST /api/fidelity/rewards (4 varianti: DISCOUNT, FREE_PRODUCT,
        CREDIT, COUPON — stesso endpoint, campo rewardType cambia)
    """

    def test_lista_premi_status_200(self, api_context):
        response = api_context.get("/api/fidelity/rewards")
        assert_status(response, 200)

    def test_config_ricarica_prepagate_status_200(self, api_context):
        response = api_context.get("/api/fidelity/topup-config")
        assert_status(response, 200)

    def test_aggiorna_switch_mostra_in_cassa_status_200(self, api_context):
        response = api_context.put(
            "/api/fidelity/topup-config", data={"showOnlyRedeemableRewards": True}
        )
        assert_status(response, 200)

    def test_aggiorna_switch_avvisa_in_cassa_status_200(self, api_context):
        response = api_context.put(
            "/api/fidelity/topup-config", data={"rewardReachedAlertEnabled": True}
        )
        assert_status(response, 200)

    def test_ricerca_prodotti_status_200(self, api_context):
        response = api_context.get(
            "/v1/products/search", params={"q": "Pollo alla Cacciatora", "limit": 50}
        )
        assert_status(response, 200)

    def test_crea_premio_sconto_status_200(self, api_context, faker):
        payload = _payload_base(
            faker,
            rewardType="DISCOUNT",
            discountType=faker.random_element(elements=("FIXED", "PERCENT")),
        )
        response = api_context.post("/api/fidelity/rewards", data=payload)
        assert_status(response, 200)
        assert_field(response.json(), "name")

    def test_crea_premio_prodotto_gratis_status_200(self, api_context, faker):
        payload = _payload_base(
            faker, rewardType="FREE_PRODUCT", freeProductSku="SKU-961197"
        )
        response = api_context.post("/api/fidelity/rewards", data=payload)
        assert_status(response, 200)
        assert_field(response.json(), "name")

    def test_crea_premio_credito_status_200(self, api_context, faker):
        payload = _payload_base(
            faker,
            rewardType="CREDIT",
            creditAmount=round(faker.pyfloat(min_value=1, max_value=100, right_digits=2), 2),
        )
        response = api_context.post("/api/fidelity/rewards", data=payload)
        assert_status(response, 200)
        assert_field(response.json(), "name")

    def test_crea_premio_coupon_status_200(self, api_context, faker):
        payload = _payload_base(
            faker,
            rewardType="COUPON",
            couponSpec={
                "valueType": "PERCENT",
                "value": faker.random_int(min=1, max=50),
                "minOrderAmount": round(faker.pyfloat(min_value=0, max_value=50, right_digits=2), 2),
                "freeProductSku": "",
                "validDays": faker.random_int(min=1, max=90),
                "maxUsage": faker.random_int(min=1, max=100),
            },
        )
        response = api_context.post("/api/fidelity/rewards", data=payload)
        assert_status(response, 200)
        assert_field(response.json(), "name")

    def test_lista_premi_senza_auth_401(self, api_context_no_auth):
        assert_unauthorized(api_context_no_auth, "get", "/api/fidelity/rewards")

    def test_crea_premio_senza_auth_401(self, api_context_no_auth, faker):
        payload = _payload_base(faker)
        assert_unauthorized(
            api_context_no_auth, "post", "/api/fidelity/rewards", data=payload
        )


# per eseguire: pytest tests/api/6_fidelity/test_premi_api.py -v
# per eseguire lo script: $env:API_DISCOVERY=1; pytest tests/6_fidelity/test_premi.py --headed -s