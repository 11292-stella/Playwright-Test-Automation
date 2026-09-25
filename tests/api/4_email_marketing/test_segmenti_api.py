import pytest
from support.api_helpers import assert_status, assert_unauthorized, assert_field


@pytest.fixture
def segmento_email(api_context, faker):
    """
    Crea un segmento/audience dinamico per il canale email con dati faker
    per garantire l'isolamento dei test.
    """
    payload = {
        "name": f"Segmento Test {faker.word()} {faker.random_int(min=1000, max=9999)}",
        "description": faker.sentence(),
        "type": "dynamic",
        "channel": "email",
        "filters": {
            "tags": ["test"],
            "customerGroup": "Nuovi clienti",
            "language": "it",
            "fidelityPointsMin": 100,
            "fidelityPointsMax": 500,
        },
    }
    response = api_context.post("/api/marketing/audiences", data=payload)
    assert_status(response, 200)
    return response.json()


def _extract_audience_id(segmento: dict) -> str:
    """Estragga l'ID del segmento provando le chiavi più comuni."""
    for candidate in ("id", "_id", "audienceId", "segmentId"):
        if candidate in segmento:
            return segmento[candidate]
    raise KeyError(
        f"Nessuna chiave ID trovata nel segmento. Chiavi disponibili: {list(segmento.keys())}"
    )


class TestSegmentiAPI:
    """
    Test API per il modulo Email Marketing > Segmenti (audiences).
    Endpoint rilevati tramite API discovery:
      - GET  /api/marketing/audiences
      - GET  /api/marketing/audiences/schema
      - GET  /api/custom-fields/entity/customer/descriptors
      - POST /api/marketing/audiences
    """

    def test_lista_audiences_status_200(self, api_context):
        """Verifica il recupero della lista dei segmenti/audiences."""
        response = api_context.get(
            "/api/marketing/audiences", params={"includeArchived": "false"}
        )
        assert_status(response, 200)

    def test_schema_audiences_status_200(self, api_context):
        """Verifica l'endpoint dello schema dei filtri dei segmenti."""
        response = api_context.get("/api/marketing/audiences/schema")
        assert_status(response, 200)

    def test_customer_descriptors_status_200(self, api_context):
        """Verifica l'ottenimento dei campi personalizzati per la segmentazione clienti."""
        response = api_context.get(
            "/api/custom-fields/entity/customer/descriptors", params={"locale": "it"}
        )
        assert_status(response, 200)

    def test_crea_segmento_status_200(self, segmento_email):
        """Verifica che la creazione di un segmento restituisca i dati attesi."""
        assert_field(segmento_email, "name")

    def test_lista_audiences_senza_auth_401(self, api_context_no_auth):
        """Verifica la protezione 401 Unauthorized sugli endpoint dei segmenti."""
        assert_unauthorized(
            api_context_no_auth,
            "get",
            "/api/marketing/audiences",
            params={"includeArchived": "false"},
        )

    def test_crea_segmento_senza_auth_401(self, api_context_no_auth, faker):
        """Verifica la protezione 401 per la creazione del segmento."""
        payload = {
            "name": f"Segmento Test {faker.word()}",
            "type": "dynamic",
            "channel": "email",
        }
        assert_unauthorized(
            api_context_no_auth, "post", "/api/marketing/audiences", data=payload
        )


# per avviare test: pytest tests/api/4_email_marketing/test_segmenti_api.py -v

# per avviare script: $env:API_DISCOVERY=1; pytest tests/4_email_marketing/test_segmenti.py --headed -s