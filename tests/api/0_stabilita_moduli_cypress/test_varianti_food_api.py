import json

import pytest
from support.api_helpers import assert_status, assert_unauthorized, assert_field


def _payload_prodotto_con_varianti(sku: str, nome: str, group_id: str, option_id: str, group_nome: str) -> dict:
    """Costruisce il payload di creazione prodotto (type=DISH) con un
    gruppo di varianti (variantGroups + variantsConfigJson)."""
    variants_config = {
        "groups": [
            {
                "id": group_id,
                "name": group_nome,
                "type": "add",
                "required": True,
                "minSelection": 1,
                "maxSelection": 4,
                "options": [{"id": option_id, "priceDelta": 0}],
            }
        ]
    }
    return {
        "sku": sku,
        "name": nome,
        "description": "",
        "labelIngredients": "",
        "customData": {},
        "type": "DISH",
        "categoryId": None,
        "fiscalDepartmentId": None,
        "fiscalRules": None,
        "fiscalRulesOverridden": False,
        "price": 0,
        "cost": 0,
        "vatRate": 10,
        "uom": "PZ",
        "productionCategoryId": None,
        "isSaleable": True,
        "isStockable": False,
        "isPurchasable": False,
        "isModifier": False,
        "active": True,
        "saleSuspended": False,
        "saleSuspendedReason": None,
        "mediaId": None,
        "colorHex": None,
        "variantGroups": [group_id],
        "variantMatrix": None,
        "recipeData": {"bom": []},
        "inventoryData": {},
        "purchaseData": {"suppliers": []},
        "salesData": {},
        "tsConfig": None,
        "variantsConfigJson": json.dumps(variants_config),
    }


@pytest.fixture
def prodotto_con_variante_di_test(api_context, faker):
    """
    Crea un prodotto (type=DISH) con un gruppo di varianti proprio,
    con id/nome univoci per il test corrente (gli id gruppo/opzione nel
    frontend sono generati come `grp_<timestamp>_<random>` / `opt_...`,
    qui basta che siano univoci nell'ambito del payload).
    """
    suffisso = faker.unique.bothify(text="????####")
    sku = f"VAR-{suffisso.upper()}"
    nome = f"Prodotto Variante Test {faker.unique.word()}"
    group_id = f"grp_test_{suffisso}"
    option_id = f"opt_test_{suffisso}"
    group_nome = f"Gruppo Test {faker.unique.word()}"

    response = api_context.post(
        "/v1/products",
        data=_payload_prodotto_con_varianti(sku, nome, group_id, option_id, group_nome),
    )
    assert_status(response, 200)
    return response.json()


class TestVariantiFoodAPI:
    """
    Test API per il modulo Varianti Food (mod_0_stabilita_moduli_cypress).
    Endpoint: GET /v1/variant-groups, GET /v1/variants,
    POST /v1/products (variantGroups + variantsConfigJson),
    GET /v1/products.
    Individuati con support/discover_endpoints.py mentre si creava un
    prodotto con un gruppo di varianti a mano.
    """

    def test_lista_gruppi_varianti_status_200(self, api_context):
        response = api_context.get("/v1/variant-groups")
        assert_status(response, 200)

    def test_lista_varianti_status_200(self, api_context):
        response = api_context.get("/v1/variants")
        assert_status(response, 200)

    def test_crea_prodotto_con_variante_status_200(self, prodotto_con_variante_di_test):
        assert_field(prodotto_con_variante_di_test, "type", "DISH")
        assert_field(prodotto_con_variante_di_test, "variantGroups")

    def test_lista_prodotti_status_200(self, api_context):
        response = api_context.get(
            "/v1/products", params={"page": "1", "pageSize": "50", "search": ""}
        )
        assert_status(response, 200)

    def test_lista_gruppi_varianti_senza_auth_401(self, api_context_no_auth):
        assert_unauthorized(api_context_no_auth, "get", "/v1/variant-groups")

    def test_crea_prodotto_con_variante_senza_auth_401(self, api_context_no_auth):
        payload = _payload_prodotto_con_varianti(
            "VAR-NOAUTH", "Prodotto No Auth", "grp_noauth", "opt_noauth", "Gruppo No Auth"
        )
        assert_unauthorized(api_context_no_auth, "post", "/v1/products", data=payload)

        # per eseguire: pytest tests/api/0_stabilita_moduli_cypress/test_varianti_food_api.py -v
        # per eseguire script per endpoint: python -m support.discover_endpoints