import pytest
from datetime import date
from support.api_helpers import assert_status, assert_unauthorized


TIPI_REPORT = ["autoconsumo", "pasti-dipendenti", "addestramento"]


class TestChiusureNonRiscosseAPI:
    """
    Test API per il modulo Report & Analytics > Chiusure Non Riscosse
    (mod_7_report_e_analytics).
    Endpoint individuati con l'API discovery agganciata al test E2E
    esistente (tests/7_report_e_analytics/test_chiusure_non_riscosse.py):
      - GET /api/reports/{tipo}/preview?year=&month=  (per ciascuno dei
        3 tipi di chiusura: autoconsumo, pasti-dipendenti, addestramento)
      - GET /api/reports/{tipo}?year=  (report generati, stesso set di
        tipi)
    """

    @pytest.mark.parametrize("tipo", TIPI_REPORT)
    def test_preview_report_status_200(self, api_context, tipo):
        oggi = date.today()
        response = api_context.get(
            f"/api/reports/{tipo}/preview",
            params={"year": oggi.year, "month": oggi.month},
        )
        assert_status(response, 200)

    @pytest.mark.parametrize("tipo", TIPI_REPORT)
    def test_lista_report_generati_status_200(self, api_context, tipo):
        oggi = date.today()
        response = api_context.get(f"/api/reports/{tipo}", params={"year": oggi.year})
        assert_status(response, 200)

    @pytest.mark.parametrize("tipo", TIPI_REPORT)
    def test_preview_report_senza_auth_401(self, api_context_no_auth, tipo):
        oggi = date.today()
        assert_unauthorized(
            api_context_no_auth,
            "get",
            f"/api/reports/{tipo}/preview",
            params={"year": oggi.year, "month": oggi.month},
        )


# per eseguire: pytest tests/api/7_report_e_analytics/test_chiusure_non_riscosse_api.py -v
# per eseguire lo script: $env:API_DISCOVERY=1; pytest tests/7_report_e_analytics/test_chiusure_non_riscosse.py --headed -s