import os
from support.api_helpers import assert_status, assert_unauthorized, assert_field

TOBACCO_ORDER_ID_TEST = os.getenv("TOBACCO_ORDER_ID_TEST", "000000000000000000000003")


class TestDdtTabacchiAPI:
    """
    Test API per il modulo DDT Tabacchi (mod_0_stabilita_moduli_cypress).
    Endpoint: POST /api/tobacco-supplier-ddts/from-order
    """

    def test_crea_ddt_da_ordine_gia_usato_e_idempotente(self, api_context):
        payload = {"tobaccoOrderId": TOBACCO_ORDER_ID_TEST, "ddtDate": "2026-08-28"}
        response = api_context.post("/api/tobacco-supplier-ddts/from-order", data=payload)
        assert_status(response, 200)
        assert_field(response.json(), "reused", True)

    def test_crea_ddt_senza_auth_401(self, api_context_no_auth):
        payload = {"tobaccoOrderId": TOBACCO_ORDER_ID_TEST, "ddtDate": "2026-08-28"}
        assert_unauthorized(api_context_no_auth, "post", "/api/tobacco-supplier-ddts/from-order", data=payload)

        # per eseguire: pytest tests/api/0_stabilita_moduli_cypress/test_ddt_tabacchi_api.py -v