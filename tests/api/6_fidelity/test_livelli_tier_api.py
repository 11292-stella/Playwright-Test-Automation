import pytest
from support.api_helpers import assert_status, assert_unauthorized, assert_field


class TestLivelliTierAPI:
    """
    Test API per il modulo Fidelity > Livelli Tier (mod_6_fidelity).
    Endpoint individuati con l'API discovery agganciata al test E2E
    esistente (tests/6_fidelity/test_livelli_tier.py):
      - GET  /api/fidelity/tiers
      - GET  /api/listini
      - POST /api/fidelity/tiers
    """

    def test_lista_tier_status_200(self, api_context):
        response = api_context.get("/api/fidelity/tiers")
        assert_status(response, 200)

    def test_lista_listini_status_200(self, api_context):
        response = api_context.get("/api/listini")
        assert_status(response, 200)

    def test_crea_tier_status_200(self, api_context, faker):
        payload = {
            "name": f"Tier {faker.unique.word().capitalize()}",
            "level": faker.random_int(min=1, max=20),
            "pointsThreshold": faker.random_int(min=100, max=5000),
            "pointsMultiplier": round(faker.pyfloat(min_value=1, max_value=3, right_digits=1), 1),
            "discountPercent": faker.random_int(min=0, max=30),
            "retentionPeriod": faker.random_int(min=1, max=12),
            "color": faker.random_element(elements=("amber", "blue", "green", "purple")),
            "icon": "mdi-trophy",
            "priceListId": None,
        }
        response = api_context.post("/api/fidelity/tiers", data=payload)
        assert_status(response, 200)
        assert_field(response.json(), "name")

    def test_lista_tier_senza_auth_401(self, api_context_no_auth):
        assert_unauthorized(api_context_no_auth, "get", "/api/fidelity/tiers")

    def test_crea_tier_senza_auth_401(self, api_context_no_auth, faker):
        payload = {
            "name": f"Tier {faker.unique.word().capitalize()}",
            "level": faker.random_int(min=1, max=20),
            "pointsThreshold": faker.random_int(min=100, max=5000),
        }
        assert_unauthorized(
            api_context_no_auth, "post", "/api/fidelity/tiers", data=payload
        )


# per eseguire: pytest tests/api/6_fidelity/test_livelli_tier_api.py -v
# per eseguire lo script: $env:API_DISCOVERY=1; pytest tests/6_fidelity/test_livelli_tier.py --headed -s