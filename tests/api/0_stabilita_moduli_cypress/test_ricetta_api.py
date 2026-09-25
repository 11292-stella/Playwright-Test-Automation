import os
import pytest
from support.api_helpers import assert_status, assert_unauthorized, assert_field


# Ingrediente noto usato per costruire il BOM (bill of materials) della
# ricetta. Non è creabile via API in questa suite (endpoint /api/ingredients
# è read-only lato test, come i Fornitori): stesso approccio del test
# Fornitori, che cerca per nome un fornitore esistente invece di crearne uno.
INGREDIENTE_ID = os.getenv("INGREDIENTE_ID_TEST", "000000000000000000000001")
INGREDIENTE_SKU = "ING-64YM76"
INGREDIENTE_NOME = "Basilico Fresco 0080"


def _payload_ricetta(sku: str, nome: str) -> dict:
    """Costruisce il payload di creazione prodotto/ricetta (type=DISH),
    con un solo ingrediente nel BOM (recipeData.bom)."""
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
        "cost": 12.5,
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
        "variantGroups": [],
        "variantMatrix": None,
        "recipeData": {
            "bom": [
                {
                    "ingredientId": INGREDIENTE_ID,
                    "ingredientSku": INGREDIENTE_SKU,
                    "productId": INGREDIENTE_ID,
                    "sku": INGREDIENTE_SKU,
                    "productSku": INGREDIENTE_SKU,
                    "name": INGREDIENTE_NOME,
                    "productName": INGREDIENTE_NOME,
                    "uom": "kg",
                    "baseUom": "kg",
                    "density": 0.92,
                    "quantity": 1,
                    "unitCost": 12.5,
                    "removable": None,
                    "isSemiFinished": False,
                }
            ]
        },
        "inventoryData": {},
        "purchaseData": {"suppliers": []},
        "salesData": {},
        "tsConfig": None,
    }


@pytest.fixture
def ricetta_di_test(api_context, faker):
    """
    Crea una ricetta (prodotto type=DISH con un ingrediente nel BOM) con
    sku/nome univoci per il test corrente, così non si riusa/consuma un
    prodotto creato a mano nel browser.
    """
    sku = f"REC-{faker.unique.bothify(text='??####').upper()}"
    nome = f"Ricetta Test {faker.unique.word()}"
    response = api_context.post("/v1/products", data=_payload_ricetta(sku, nome))
    assert_status(response, 200)
    return response.json()


class TestRicettaAPI:
    """
    Test API per il modulo Ricetta (mod_0_stabilita_moduli_cypress).
    Endpoint: GET /api/ingredients, POST /v1/products (recipeData.bom),
    GET /v1/products.
    Individuati con support/discover_endpoints.py mentre si creava una
    ricetta a mano (ricerca ingrediente + salvataggio prodotto).
    """

    def test_lista_ingredienti_status_200(self, api_context):
        response = api_context.get("/api/ingredients", params={"pageSize": "20"})
        assert_status(response, 200)

    def test_ricerca_ingrediente_per_nome_status_200(self, api_context):
        response = api_context.get(
            "/api/ingredients",
            params={"pageSize": "20", "search": INGREDIENTE_NOME},
        )
        assert_status(response, 200)

    def test_crea_ricetta_status_200(self, ricetta_di_test):
        assert_field(ricetta_di_test, "type", "DISH")
        assert_field(ricetta_di_test, "recipeData")

    def test_lista_prodotti_status_200(self, api_context):
        response = api_context.get(
            "/v1/products", params={"page": "1", "pageSize": "50", "search": ""}
        )
        assert_status(response, 200)

    def test_lista_ingredienti_senza_auth_401(self, api_context_no_auth):
        assert_unauthorized(
            api_context_no_auth, "get", "/api/ingredients", params={"pageSize": "20"}
        )

    def test_crea_ricetta_senza_auth_401(self, api_context_no_auth):
        payload = _payload_ricetta("REC-NOAUTH", "Ricetta No Auth")
        assert_unauthorized(api_context_no_auth, "post", "/v1/products", data=payload)

        # per eseguire: pytest tests/api/0_stabilita_moduli_cypress/test_ricetta_api.py -v
        # per eseguire script per endpoint: python -m support.discover_endpoints