import pytest
from support.api_helpers import assert_status, assert_unauthorized, assert_field


def _extract_id(obj: dict, candidates=("campaignId", "audienceId", "id", "_id")) -> str:
    """
    Le risposte di questo backend non usano sempre "id" come nome di
    campo (vedi test_web_app_tavolo_catalogo_api.py). Proviamo le
    varianti più comuni; se nessuna esiste, l'errore mostra tutte le
    chiavi reali della risposta così scegliamo quella giusta al volo
    invece di dover rilanciare a mano con -s.
    """
    for candidate in candidates:
        if candidate in obj:
            return obj[candidate]
    raise KeyError(f"Nessuna chiave id nota trovata. Chiavi disponibili: {list(obj.keys())}")


@pytest.fixture
def campagna_di_test(api_context, faker):
    """
    Crea una campagna email con nome univoco, così i test a valle
    (get singola, stats, update, preview, invio di prova) hanno una
    campagna propria invece di dipendere da quelle create a mano nel
    browser.
    """
    payload = {
        "name": f"pytest {faker.unique.word()}",
        "channel": "email",
        "templateId": "blank",
    }
    response = api_context.post("/api/marketing/campaigns", data=payload)
    assert_status(response, 200)
    return response.json()


@pytest.fixture
def prima_audience(api_context):
    """
    Recupera la prima audience disponibile, da riusare come
    audienceId nel test di aggiornamento campagna e nella preview
    audience — invece di hardcodare un id che può non esistere più
    nel tenant demo.
    """
    response = api_context.get("/api/marketing/audiences", params={"includeArchived": "false"})
    assert_status(response, 200)
    body = response.json()
    lista = body if isinstance(body, list) else body.get("items") or body.get("data") or []
    assert lista, f"Nessuna audience trovata nel tenant demo, risposta: {body}"
    return _extract_id(lista[0])


class TestCampagneMarketingAPI:
    """
    Test API per il modulo Email Marketing > Campagne
    (mod_4_email_marketing).
    Endpoint individuati con l'API discovery agganciata al test E2E
    esistente (tests/4_email_marketing/test_campagne_marketing.py):
      - GET  /api/marketing/campaigns
      - GET  /api/marketing/campaigns/templates
      - GET  /api/marketing/campaigns/variables
      - GET  /api/marketing/campaigns/{id}
      - GET  /api/marketing/campaigns/{id}/stats
      - GET  /api/marketing/audiences
      - POST /api/marketing/campaigns
      - POST /api/marketing/audiences/preview
      - POST /api/marketing/campaigns/{id}/preview
      - POST /api/marketing/campaigns/{id}/test
      - PUT  /api/marketing/campaigns/{id}
    """

    def test_lista_campagne_status_200(self, api_context):
        response = api_context.get("/api/marketing/campaigns")
        assert_status(response, 200)

    def test_lista_template_campagne_status_200(self, api_context):
        response = api_context.get("/api/marketing/campaigns/templates")
        assert_status(response, 200)

    def test_lista_variabili_campagna_status_200(self, api_context):
        response = api_context.get("/api/marketing/campaigns/variables")
        assert_status(response, 200)

    def test_lista_audiences_status_200(self, api_context):
        response = api_context.get("/api/marketing/audiences", params={"includeArchived": "false"})
        assert_status(response, 200)

    def test_crea_campagna_status_200(self, campagna_di_test):
        assert_field(campagna_di_test, "name")

    def test_recupera_campagna_status_200(self, api_context, campagna_di_test):
        campagna_id = _extract_id(campagna_di_test)
        response = api_context.get(f"/api/marketing/campaigns/{campagna_id}")
        assert_status(response, 200)

    def test_statistiche_campagna_status_200(self, api_context, campagna_di_test):
        campagna_id = _extract_id(campagna_di_test)
        response = api_context.get(f"/api/marketing/campaigns/{campagna_id}/stats")
        assert_status(response, 200)

    def test_preview_audience_status_200(self, api_context, prima_audience):
        response = api_context.post(
            "/api/marketing/audiences/preview", data={"audienceId": prima_audience}
        )
        assert_status(response, 200)

    def test_aggiorna_campagna_status_200(self, api_context, campagna_di_test, prima_audience, faker):
        campagna_id = _extract_id(campagna_di_test)
        payload = {
            "name": campagna_di_test["name"],
            "subject": faker.sentence(),
            "preheader": faker.sentence(),
            "bodyHtml": f"<p>{faker.paragraph()}</p>",
            "audienceId": prima_audience,
            "fromName": faker.name(),
            "replyTo": faker.email(),
            "channel": "email",
            "whatsappTemplateSid": None,
        }
        response = api_context.put(f"/api/marketing/campaigns/{campagna_id}", data=payload)
        assert_status(response, 200)

    def test_preview_campagna_status_200(self, api_context, campagna_di_test):
        campagna_id = _extract_id(campagna_di_test)
        response = api_context.post(f"/api/marketing/campaigns/{campagna_id}/preview", data={})
        assert_status(response, 200)

    def test_invio_prova_campagna_status_200(self, api_context, campagna_di_test, faker):
        """
        L'endpoint /test rifiuta una campagna senza oggetto/contenuto
        (422 CAMPAIGN_INCOMPLETE), quindi prima la completiamo con una
        PUT: campagna_di_test è function-scoped, ogni test parte da una
        campagna vuota propria, non riusa quella di
        test_aggiorna_campagna_status_200.
        """
        campagna_id = _extract_id(campagna_di_test)
        update_payload = {
            "name": campagna_di_test["name"],
            "subject": faker.sentence(),
            "preheader": faker.sentence(),
            "bodyHtml": f"<p>{faker.paragraph()}</p>",
            "channel": "email",
        }
        response = api_context.put(f"/api/marketing/campaigns/{campagna_id}", data=update_payload)
        assert_status(response, 200)

        response = api_context.post(
            f"/api/marketing/campaigns/{campagna_id}/test", data={"to": faker.email()}
        )
        assert_status(response, 200)

    def test_lista_campagne_senza_auth_401(self, api_context_no_auth):
        assert_unauthorized(api_context_no_auth, "get", "/api/marketing/campaigns")

 
# per eseguire: pytest tests/api/4_email_marketing/test_campagne_marketing_api.py -v
# per eseguire lo script: $env:API_DISCOVERY=1 pytest tests/4_email_marketing/test_campagne_marketing.py --headed -s

