import pytest
from support.auth import login_utente
from support.config import API_BASE_URL, BASE_URL


@pytest.fixture(scope="session")
def api_auth_headers(browser):
    """
    Fa login via UI e intercetta gli header reali (Authorization Bearer,
    x-tenant-id, x-reseller-code) mandati dal frontend verso l'API dopo
    il login, per riusarli nelle chiamate dirette di api_context.
    NB: il token scade dopo ~30 min (vita breve tipica di un access
    token Keycloak): se la suite dura più a lungo, i test API possono
    iniziare a fallire con 401 e la fixture andrà rilanciata.
    """
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
    page.goto(BASE_URL)          # forza il caricamento della dashboard così partono chiamate API
    page.wait_for_timeout(2000)  # dai tempo alle richieste di partire

    context.close()

    if "authorization" not in captured:
        raise RuntimeError(
            "Non sono riuscito a intercettare l'header Authorization dopo il login. "
            "Serve navigare verso una pagina che faccia sicuramente una chiamata API."
        )
    return captured


@pytest.fixture(scope="session")
def api_context(playwright, api_auth_headers):
    """
    Contesto per chiamate API dirette, autenticato con gli header
    catturati da api_auth_headers. Punta a API_BASE_URL (dominio API,
    diverso dal dominio della UI).
    """
    context = playwright.request.new_context(
        base_url=API_BASE_URL,
        extra_http_headers=api_auth_headers,
    )
    yield context
    context.dispose()


@pytest.fixture(scope="session")
def api_context_no_auth(playwright):
    """
    Contesto per chiamate API senza autenticazione.
    Da usare per verificare i casi 401/403 quando manca il token.
    """
    context = playwright.request.new_context(base_url=API_BASE_URL)
    yield context
    context.dispose()