# Playwright Test Automation — gestionale web per la ristorazione

Suite di test automatizzati **E2E + API** scritta in **Python con Playwright e pytest**, per un gestionale web multi-tenant per la ristorazione (frontend Vue 3 / Vuetify, autenticazione Keycloak).

Il progetto nasce dalla **migrazione di una suite Cypress** esistente e la estende con una **suite API** che testa direttamente il backend, senza browser.

> ℹ️ Questa è una **versione pubblica sanitizzata**: URL, tenant, credenziali e ID reali sono stati rimossi o sostituiti con variabili d'ambiente e valori demo.

---

## Stack

| Ambito | Tecnologia |
|---|---|
| Linguaggio | Python 3 |
| Framework di test | pytest |
| Automazione browser e API | Playwright (`sync_api`, `APIRequestContext`) |
| Dati di test | Faker |
| Report | Allure, JUnit XML, pytest-html |
| CI/CD | GitLab CI (immagine Docker ufficiale Playwright Python) |

---

## Numeri

| Suite | File di test | Test |
|---|---|---|
| E2E (UI) | 49 | ~70 |
| API | 37 | **226** |

Moduli coperti: gestione catene, configurazione ristorante (web app asporto e tavolo), delivery (Deliveroo, Just Eat, Uber Eats, Glovo, Deliverect), fidelity, email marketing, report e analytics, controllo di gestione, anagrafiche e magazzino.

---

## Struttura

```
.
├── pages/                  # Page Object Model, una cartella per modulo
│   └── base_page.py        # helper condivisi per i componenti Vuetify
├── support/
│   ├── auth.py             # login
│   ├── config.py           # legge le variabili da .env
│   ├── api_helpers.py      # assert_status, assert_unauthorized, assert_field, debug_body
│   ├── api_logger.py       # logger delle chiamate API (API discovery)
│   └── discover_endpoints.py
├── utils/
│   └── test_data.py        # generatori di dati di test "usa e getta"
├── tests/
│   ├── conftest.py         # fixture E2E (sessione di login, pagina autenticata)
│   ├── 0_…/ … 8_…/         # test E2E per modulo
│   └── api/
│       ├── conftest.py     # fixture API (header catturati, contesti con e senza token)
│       └── 0_…/ … 7_…/     # test API per modulo
├── pytest.ini
└── .gitlab-ci.yml
```

---

## Suite E2E

### Page Object Model con `BasePage`

Ogni pagina ha la sua classe; i comportamenti ripetuti sui componenti Vuetify stanno in `BasePage`:

- gestione dei dropdown Vuetify in due varianti (`force=True` e `_no_force`)
- `seleziona_option_casuale_dropdown` e `cicla_tutte_le_opzioni_dropdown` per test data-driven sulle opzioni
- `salva_html_pagina`: salva l'HTML reale della pagina prima di scrivere i locator di un componente sconosciuto

### Login una sola volta per sessione

```python
@pytest.fixture(scope="session")
def storage_state_path(browser):
    context = browser.new_context()
    page = context.new_page()
    login_utente(page)
    context.storage_state(path=STORAGE_STATE_PATH)   # equivalente di cy.session()
    context.close()
    return STORAGE_STATE_PATH


@pytest.fixture
def authenticated_page(browser, storage_state_path):
    context = browser.new_context(storage_state=storage_state_path)
    page = context.new_page()
    page.goto(BASE_URL)
    yield page
```

### Pattern ricorrenti

- **Locator limitati al dialog aperto**: `page.get_by_role("dialog")` per evitare di prendere elementi dietro la modale.
- **Dati "usa e getta"**: ogni test crea i propri dati con nomi generati (es. `ChainTestData.genera_dati_nuova_catena()`), niente nomi fissi nel codice.
- **Controllo del tenant**: un'asserzione verifica di essere sul tenant di test prima di modificare dati.

---

## Suite API

I test API chiamano direttamente il backend con `APIRequestContext`, senza aprire pagine.

### Autenticazione: header catturati dal login reale

Il backend richiede un token Keycloak più header di contesto (tenant). Invece di ricostruirli a mano, una fixture di sessione fa il login dalla UI e **intercetta gli header reali** che il frontend manda alle API:

```python
@pytest.fixture(scope="session")
def api_auth_headers(browser):
    captured = {}
    context = browser.new_context()
    page = context.new_page()

    def handle_request(request):
        auth = request.headers.get("authorization")
        if auth and API_BASE_URL in request.url:
            captured["authorization"] = auth
            captured["x-tenant-id"] = request.headers.get("x-tenant-id")
            captured["x-reseller-code"] = request.headers.get("x-reseller-code")

    page.on("request", handle_request)
    login_utente(page)
    page.goto(BASE_URL)
    ...
    return captured


@pytest.fixture(scope="session")
def api_context(playwright, api_auth_headers):
    context = playwright.request.new_context(
        base_url=API_BASE_URL,
        extra_http_headers=api_auth_headers,
    )
    yield context
    context.dispose()


@pytest.fixture(scope="session")
def api_context_no_auth(playwright):
    # stesso base_url, nessun token: per verificare i 401
    context = playwright.request.new_context(base_url=API_BASE_URL)
    yield context
    context.dispose()
```

### Struttura di un test API

Ogni endpoint viene verificato sia nel caso positivo sia **senza autenticazione**:

```python
class TestBuoniMultiusoAPI:

    def test_lista_buoni_status_200(self, api_context):
        response = api_context.get("/api/gift-cards")
        assert_status(response, 200)

    def test_emetti_buono_status_200(self, api_context, faker):
        payload = {
            "value": faker.random_int(min=10, max=200),
            "validDays": faker.random_int(min=30, max=365),
        }
        response = api_context.post("/api/gift-cards/issue", data=payload)
        assert_status(response, 200)

    def test_lista_buoni_senza_auth_401(self, api_context_no_auth):
        assert_unauthorized(api_context_no_auth, "get", "/api/gift-cards")
```

### API discovery: mappare gli endpoint senza documentazione

Il backend non aveva una documentazione delle API. Con la variabile `API_DISCOVERY=1`, la fixture `authenticated_page` aggancia un logger a ogni test E2E e salva tutte le chiamate API che la UI fa durante il flusso:

```powershell
$env:API_DISCOVERY=1
pytest tests/6_fidelity/test_buoni_multiuso.py --headed -s
# → reports/api-discovery/<nome_test>.log
```

Da quei log sono nati i test API di ogni modulo.

### Bug noti tracciati con `xfail`

Quando un test incontra un bug noto del backend, lo segnala in modo esplicito invece di fallire senza spiegazione:

```python
if response.status != 200:
    pytest.xfail(
        "Emissione fallita - probabile BUG NOTO backend "
        "(indice UNIQUE non-sparse su idempotencyKey). "
        f"Status: {response.status}. Body: {debug_body(response)}"
    )
```

Esempio reale: un indice UNIQUE non-sparse su `idempotencyKey` faceva andare a buon fine solo la prima emissione di un buono regalo; le successive fallivano lato server.

### Test data-driven

```python
# TIPI_REPORT = tipi di chiusura: autoconsumo, pasti-dipendenti, addestramento
@pytest.mark.parametrize("tipo", TIPI_REPORT)
def test_preview_report_status_200(self, api_context, tipo):
    oggi = date.today()
    response = api_context.get(
        f"/api/reports/{tipo}/preview",
        params={"year": oggi.year, "month": oggi.month},
    )
    assert_status(response, 200)
```

### Valori di test da variabili d'ambiente

Codici di catena, tenant e ID usati dai test si leggono da `.env`, con un valore demo di default:

```python
CODICE_CATENA_TEST = os.getenv("CODICE_CATENA_TEST", "demo_catena_test")
```

---

## Configurazione

Crea un file `.env` nella root (non versionato):

```env
EMAIL=utente@example.com
PASSWORD=********
BASE_URL=https://app.example.com
API_BASE_URL=https://api.example.com
TENANT_LABEL=Ristorante Demo

# valori usati da alcuni test API
CODICE_CATENA_TEST=demo_catena_test
TENANT_SORGENTE_TEST=demo_tenant_test
SITE_ID_TEST=Ristorante Demo (demo_tenant_test)
INGREDIENTE_ID_TEST=000000000000000000000001
TOBACCO_ORDER_ID_TEST=000000000000000000000003
```

## Esecuzione

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
playwright install

# tutta la suite
pytest

# solo le API
pytest tests/api -v

# un modulo
pytest tests/api/6_fidelity -v

# report
pytest tests/api --junitxml=reports/junit.xml --alluredir=reports/allure-results
allure serve reports/allure-results
```

## CI/CD

La pipeline GitLab CI usa l'immagine Docker ufficiale di Playwright per Python, esegue le suite e pubblica i report JUnit e Allure come artifact.

---

## Note

- Il token Keycloak dura circa 30 minuti: nelle esecuzioni molto lunghe i test API possono iniziare a rispondere 401 e la fixture va rilanciata.
- Miglioramento previsto: sostituire l'attesa fissa nella fixture di cattura degli header con un `page.wait_for_response(...)`.
